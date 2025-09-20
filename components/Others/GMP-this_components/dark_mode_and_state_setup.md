# Dark Mode & State Setup

Initializes the interface with the user's preferred color scheme and prepares shared state holders along with the DOM lookups that the rest of the analyzer relies on.

```javascript
// Dark mode setup
if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    document.documentElement.classList.add('dark');
}
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
    if (event.matches) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
});

// Global state
let currentAnalysis = null;
let currentStages = [];
let showingAllStages = false;
let gmpFileContent = null;

// DOM elements
const conceptInput = document.getElementById('conceptInput');
const gmpSelect = document.getElementById('gmpSelect');
const aiModel = document.getElementById('aiModel');
const gmpFile = document.getElementById('gmpFile');
const analyzeBtn = document.getElementById('analyzeBtn');
const clearBtn = document.getElementById('clearBtn');
const resultsSection = document.getElementById('resultsSection');
const gmpRecommendation = document.getElementById('gmpRecommendation');
const stagesContainer = document.getElementById('stagesContainer');
const showAllBtn = document.getElementById('showAllBtn');
const chatInterface = document.getElementById('chatInterface');
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendChatBtn = document.getElementById('sendChatBtn');
```
