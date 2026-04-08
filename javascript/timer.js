let hr = document.getElementById("hour");
let min = document.getElementById("min");
let sec = document.getElementById("sec");

function startTimer() {
  let h = parseInt(hr.innerText) || 0;
  let m = parseInt(min.innerText) || 0;
  let s = parseInt(sec.innerText) || 0;

  let totalSeconds = h * 3600 + m * 60 + s;

  if (totalSeconds <= 0) {
    document.getElementById("status").innerText = "Enter Time!!";
    document.getElementById("status").style.backgroundColor =
      "rgb(237, 106, 13)";
    document.getElementById("status").style.fontSize = "35px";
    return;
  }

  function tick() {
    totalSeconds--; // Subtract one second

    let newH = Math.floor(totalSeconds / 3600);
    let newM = Math.floor((totalSeconds % 3600) / 60);
    let newS = totalSeconds % 60;

    hr.innerText = newH.toString().padStart(2, "0");
    min.innerText = newM.toString().padStart(2, "0");
    sec.innerText = newS.toString().padStart(2, "0");

    if (totalSeconds > 0) {
      timerId = setTimeout(tick, 1000);
    } else {
      document.getElementById("status").innerText = "Time Up";
      document.getElementById("status").style.backgroundColor =
        "rgb(137, 237, 13)";
      document.getElementById("status").style.fontSize = "40px";
    }
  }

  setTimeout(tick, 1000);
}

function stopTimer() {
  clearTimeout(timerId); // This stops the countdown immediately
}
