
let editor = null;
let currentFile = null;

// Load list of available config files
async function loadConfigList() {
    try {
        let res = await fetch("/ui/config/list");
        let data = await res.json();

        let sel = document.getElementById("configSelect");
        sel.innerHTML = "";

        data.files.forEach(f => {
            let opt = document.createElement("option");
            opt.value = f;
            opt.innerText = f;
            sel.appendChild(opt);
        });

        if (data.files.length > 0) {
            sel.value = data.files[0];
            loadConfig();
        } else {
            document.getElementById("editorContainer").style.display = "none";
        }
    } catch (err) {
        console.error("Failed to load config list:", err);
        alert("Failed to load config list.");
    }
}

// Load a specific config file into the editor
async function loadConfig() {
    try {
        let filename = document.getElementById("configSelect").value;
        currentFile = filename;

        let res = await fetch(`/ui/config/load/${filename}`);
        let data = await res.json();

        document.getElementById("configTitle").innerText = filename;
        document.getElementById("editorContainer").style.display = "block";

        if (editor) {
            editor.setValue(data.content || "");
        } else {
            let textarea = document.getElementById("configEditor");
            textarea.value = data.content || "";
        }
    } catch (err) {
        console.error("Failed to load config file:", err);
        alert("Failed to load config file.");
    }
}

// Save current config back to the server
async function saveConfig() {
    if (!currentFile) {
        alert("No config file selected.");
        return;
    }

    let content = editor ? editor.getValue() : document.getElementById("configEditor").value;

    try:
        let res = await fetch(`/ui/config/save/${currentFile}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ content })
        });

        let data = await res.json();

        if (data.status === "ok") {
            alert("Config saved. Backup created at: " + data.backup);
        } else {
            alert("Save failed: " + (data.message || "Unknown error"));
        }
    } catch (err) {
        console.error("Failed to save config:", err);
        alert("Failed to save config.");
    }
}

// Initialize CodeMirror editor
function initConfigEditor() {
    let textarea = document.getElementById("configEditor");
    if (!textarea) return;

    editor = CodeMirror.fromTextArea(textarea, {
        lineNumbers: true,
        mode: "yaml",
        theme: "default",
        tabSize: 2,
        indentUnit: 2,
        lineWrapping: true
    });

    loadConfigList();
}

window.addEventListener("load", initConfigEditor);
