# DRBanger Enhanced Legal Research System — Component Index

The **VG-LegalApp_v5_active** canvas is a manual, six-bot workflow for legal research refinement. Users curate their source material, pair it with SST (Structured Strategic Technique) capsules, then drive the chain manually bot-by-bot while capturing state, logs, and generated improvements. This directory extracts the reusable building blocks so both builders and operators can understand what powers the experience.

## Experience Map
- **Input Configuration Tab** – Upload JSON databases, craft legal text + SST payloads, and stage prompts/injection notes before running any bots.
- **Execution & Results Tab** – Orchestrate six specialised bots (SST applicator → adversarial reviewer → international-law validator → ICC synthesiser → publication QA → SST improver) with mirrored controls and live status feedback.
- **Global Utilities** – Persistent floating "Next Bot" launcher, activity log with streaming updates, custom-instruction injectors per bot, and state save/load pipeline for migrating work between sessions.

## Key Modules Extracted
1. **Input Configuration Layout** – `input_configuration.md` captures the Tailwind layout for the File Upload Centre, legal/SST editors, and manual SST selector.
2. **Accordion Model Selector** – `model_selection.md` documents the searchable accordion used to pick a bot model from an extensive catalogue, including keyboard navigation and auto-collapse logic.
3. **Workflow Runner** – `workflow_engine.md` shows how six bot prompts are assembled, validated, and sent to Poe while synchronising UI state, timeouts, and floating-button progress.
4. **Prompt Templates** – `prompts.md` transcribes every bot mandate so operators can see the exact roles and insertion points feeding the chain.
5. **State Management Suite** – `state_management.md` details how the app serialises inputs, outputs, injected instructions, and workflow metadata for clipboard/file storage with validation safeguards.

Each module file contains two parts: the lifted template/code and a plain-language explanation so operators know what the interface affords and developers can repurpose the logic.

> ❗ **Source of truth**: `HTML Apps/Law Thesis/VG-LegalApp_v5_active.html` remains untouched. This folder only mirrors the relevant structures for documentation and reuse.
