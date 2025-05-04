var text = `{{ all_comments }}`;
var words = text.split(/\s+/);
var wordFreq = {};
words.forEach(function(w) {
    w = w.toLowerCase();
    if (w.length > 2) wordFreq[w] = (wordFreq[w] || 0) + 1;
});
var list = Object.entries(wordFreq);
WordCloud(document.getElementById('wordcloud'), { list: list, gridSize: 8, weightFactor: 8, fontFamily: 'Arial', color: 'random-dark' });
