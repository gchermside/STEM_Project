const queryString = window.location.search;
const params = new URLSearchParams(queryString);
const word= params.get("word");
const pictureOrVideo= params.get("pictureOrVideo");
document.getElementById("wordSpan").textContent=word;


console.log(word);
console.log(pictureOrVideo);