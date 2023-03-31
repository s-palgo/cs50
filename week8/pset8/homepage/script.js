const countBtn = document.getElementById('count-btn');
const timesBtnClickedPara = document.getElementById('times-btn-clicked');
let timesBtnClicked = 0;

countBtn.addEventListener('click', function() {
    timesBtnClicked += 1;
    timesBtnClickedPara.innerHTML = `Times button clicked: <span id="number-times-clicked">${timesBtnClicked}</span>`;
});