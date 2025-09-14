import os
import modal
from typing import AsyncIterable
import fastapi_poe as fp

# ——————————————————————————————————————————————————————————————
# ⚙️  Modal App & Secrets Configuration
# ——————————————————————————————————————————————————————————————
app = modal.App("poe-server-bot")
poe_secrets = modal.Secret.from_name("poe-bot-secrets")

# ——————————————————————————————————————————————————————————————
# 📦  Container Images & Dependencies
# ——————————————————————————————————————————————————————————————
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install("fastapi-poe>=0.0.64", "aiohttp", "uvicorn")
)



# ——————————————————————————————————————————————————————————————
# 🤖  The DRBanger Chain Logic - Legal Research System
# ——————————————————————————————————————————————————————————————
class ChainedBot(fp.PoeBot):
    async def get_response(self, request: fp.QueryRequest) -> AsyncIterable[fp.PartialResponse]:
        user_message = request.query[-1].content
        user_access_key = request.access_key

        # STEP 1: Parser Bot (Syntax Drain)
        yield fp.PartialResponse(text="🔍 **Parser Bot (Syntax Drain):**\n\n")
        parser_prompt = f"""ROLE: syntax_drain_parser
TASK: Extract clean tokens from ICC legal text
INPUT: {user_message}
OUTPUT: Provide only the drained token list with core legal concepts isolated.
INSTRUCTION: Strip procedural language, isolate key legal elements, provide structured token output."""

        parser_msg = fp.ProtocolMessage(role="user", content=parser_prompt)
        parser_request = request.model_copy(update={"query": [parser_msg]})
        
        parser_output = ""
        try:
            async for msg in fp.stream_request(parser_request, "VG-Rezbot", user_access_key):
                if hasattr(msg, 'text') and msg.text:
                    parser_output += msg.text
                    yield fp.PartialResponse(text=msg.text)
        except Exception as e:
            yield fp.PartialResponse(text=f"Error: Could not reach Parser Bot. {e}")
            return

        # STEP 2: Transformer Bot (SST Application)
        yield fp.PartialResponse(text="\n\n---\n\n⚡ **Transformer Bot (SST Application):**\n\n")
        
        transformer_prompt = f"""ROLE: sst_mechanical_applicator
TASK: Apply SST transformation mechanically, no interpretation
INPUT TOKENS: {parser_output}

KNOWLEDGE FILE: SST Capsule List - Select and apply ONE technique from:
- Brewing Science techniques (temperature control, fermentation, distillation)
- Chess notation systems (algebraic, FEN encoding, position analysis)
- Culinary techniques (scaling, substitution, fermentation)
- Music theory transformations (inversion, retrograde, transposition)
- Geoinformatics (projection, simplification, aggregation)
- Mathematical proof techniques (contraposition, WLOG, lemma factoring)
- Software patterns (extract method, adapter, facade)
- Pedagogical methods (chunking, scaffolding, dual coding)
- Origami techniques (collapse folding, wet-folding, precreasing)
- Military operations (SALUTE, SITREP, METT-TC)
- Narrative/mythological (archetypal re-skinning, perspective flip, genre blending)
- Translation studies (transposition, modulation, compensation)

OUTPUT: Raw transformation result applying technique to tokens.
INSTRUCTION: Select an appropriate SST technique and apply transformation mechanically without legal analysis. Map tokens through chosen SST domain directly. State which technique you're using."""

        transformer_msg = fp.ProtocolMessage(role="user", content=transformer_prompt)
        transformer_request = request.model_copy(update={"query": [transformer_msg]})
        
        transformer_output = ""
        try:
            async for msg in fp.stream_request(transformer_request, "VG-Techbot", user_access_key):
                if hasattr(msg, 'text') and msg.text:
                    transformer_output += msg.text
                    yield fp.PartialResponse(text=msg.text)
        except Exception as e:
            yield fp.PartialResponse(text=f"Error: Could not reach Transformer Bot. {e}")
            return

        # STEP 3: Synthesizer Bot (Legal Output Formatter)
        yield fp.PartialResponse(text="\n\n---\n\n📝 **Synthesizer Bot (Legal Output):**\n\n")
        synthesizer_prompt = f"""ROLE: legal_output_formatter
TASK: Generate novel ICC legal interpretation using SST-transformed concepts
INPUT: {transformer_output}
ORIGINAL ICC TEXT: {user_message}
OUTPUT: Novel interpretation of the ICC article using the SST lens.
INSTRUCTION: 
- Apply the transformed concepts BACK to understanding the ICC article
- Focus on what the SST transformation reveals about the legal text
- Do NOT create new frameworks about the SST domain itself
- Keep interpretation focused on ICC law insights
- Format: Brief interpretation (2-3 paragraphs) + methodological note
- Academic tone for supervisor email"""

        synthesizer_msg = fp.ProtocolMessage(role="user", content=synthesizer_prompt)
        synthesizer_request = request.model_copy(update={"query": [synthesizer_msg]})

        try:
            async for msg in fp.stream_request(synthesizer_request, "VG-Secbot", user_access_key):
                if hasattr(msg, 'text') and msg.text:
                    yield fp.PartialResponse(text=msg.text)
        except Exception as e:
            yield fp.PartialResponse(text=f"Error: Could not reach Synthesizer Bot. {e}")
            return

    async def get_settings(self, setting: fp.SettingsRequest) -> fp.SettingsResponse:
        return fp.SettingsResponse(
            server_bot_dependencies={
                "VG-Rezbot": 2,
                "VG-Techbot": 2,
                "VG-Secbot": 2
            },
            allow_attachments=False,
            introduction_message="🎯 DRBanger Legal Research Chain: Parser → Transformer → Synthesizer"
        )

# ——————————————————————————————————————————————————————————————
# 🚀  Deployment Entrypoint
# ——————————————————————————————————————————————————————————————
@app.function(image=image, secrets=[poe_secrets])
@modal.asgi_app()
def fastapi_entry():
    """This function connects our bot logic to Poe's servers."""
    bot = ChainedBot()

    return fp.make_app(
        bot,
        bot_name="DRBanger",
        access_key=os.environ["POE_BOT_API_KEY"]
    )
