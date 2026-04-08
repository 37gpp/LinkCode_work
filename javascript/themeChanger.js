let currentTheme = "morning";

function toggleTheme() {
  const pandaImg = document.getElementById("panda-img");
  const body = document.body;

  if (currentTheme === "morning") {
    body.style.backgroundImage = "url('night.jpg')";
    body.style.color = "white";
    pandaImg.src = "sleeping-panda.png";
    currentTheme = "night";
  } else {
    body.style.backgroundImage = "url('morning.jpg')";
    body.style.color = "black";
    pandaImg.src = "woked-panda.png";
    currentTheme = "morning";
  }
}
