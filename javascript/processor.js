"use strict";

const FocusApp = {
  tasks: [],

  init: function () {
    const input = document.getElementById("taskInput");
    const warning = document.getElementById("warning");

    input.addEventListener("keypress", (e) => {
      const blockedWords = ["reels", "scrolling", "timepass", "shorts"];

    
      const isBadWord = blockedWords.some((word) =>
        input.value.toLowerCase().includes(word),
      );

      if (isBadWord) {
        warning.innerText = "Padhle bhai Padhle!";
        
        if (e.key === "Enter") e.preventDefault();
        return;
      } else {
        warning.innerText = ""; 
      }

      if (e.key === "Enter") {
        this.addTask(input.value);
        input.value = "";
      }
    });
  },

  addTask: function (rawText) {
    
    const formatTask = (str) => ({
      text: str.trim().toUpperCase(),
      addedAt: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    });

   
    const createHTML = (taskObj) => `
        <div class="task-item">
            <span><strong>${taskObj.addedAt}</strong> - ${taskObj.text}</span>
            <span style="cursor:pointer" onclick="this.parentElement.remove()">✕</span>
        </div>`;

    if (rawText.trim().length > 0) {
      const playlist = document.getElementById("playlist");
      playlist.innerHTML += createHTML(formatTask(rawText));
    }
  },
};

FocusApp.init();
