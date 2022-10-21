# diary

to keep a diary, to make life fun

<span>choose</span>
<input type="date" id="diary" name="oh" value="new Date()" min="2022-10-20" max="new Date()">
<a id="run" href="https://draugus.github.io/diary/"
    onclick="this.href += document.getElementById('diary').value">view</a>

<button onclick="console.log(document.getElementById('diary').value)"> vvv </button>
