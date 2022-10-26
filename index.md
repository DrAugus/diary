# diary

to keep a diary, to make life fun

<span>choose</span>
<input type="date" id="diary_date_info" name="oh" value="new Date()" min="2022-10-20" max="new Date()">
<a id="run" href="https://draugus.github.io/diary/"
    onclick="this.href += 
    document.getElementById('diary_date_info').value
    .replace(/-/g, '/')">view</a>

