# canvas_componento

Purpose
- House Poe Canvas apps as canonical sources. Documentation of canvas stored in the repo as Poe Canvas Docs August 29th.md. link for documentation: https://creator.poe.com/docs/ 
- Extract features, components, and code snippets into `components/` with brief explanations of what they are and what they do.
- When files look similar in functionality, and are mostly very much identical, figure out the difference between the two or whatever number it is. Potential such files have been grouped in subfolders but not all subfolders follow that rule. We will only move sequentially so this is a stage that will be executed after components are extracted/not considered unique or good enough for extraction. 

Critical rule
- Do not edit the app HTML files. Treat them as source-of-truth artifacts only. Keeping HTML untouched avoids needless merge conflicts. All refactoring and explanations belong in `components/` and related docs.

Notes
- This repository focuses on organization and component extraction. Implementation “how-tos” may vary by contributor and are intentionally not prescribed here.
- The `components/` directory mirrors the `HTML Apps/` hierarchy so extracted bundles stay colocated with their source canvases.

## Updates

- 15-09-2025 - Added Canvas HTML files
- 20-09-2025 - Synced `components/` directory layout with `HTML Apps/` for easier navigation
