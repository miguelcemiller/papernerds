// var text = document.querySelector('.text');

// /* var needle = "Lorem";
// var text_content = text.textContent

// text_content.replace(needle, '<b>' + needle + '</b>');

// text.innerHTML = text_content; */
// var text_content =  text.textContent;

// //beginning 4, end 7
// var word_match = text_content.substring(4, 7+1); //The 'lazy' word


// var replace = word_match;
// var re = new RegExp(replace,"g");

// html.replace(re, '<em>$&</em>')


//this may just work

function wrapSubstring(sourceString, tag, startIndex, endIndex) {
    return sourceString.substring(0, startIndex)
        + "<" + tag + ">"
        + sourceString.substring(startIndex, endIndex)
        + "</" + tag + ">"
        + (endIndex ? sourceString.substring(endIndex) : "");
}

var $element = $('.text');
$element.html(wrapSubstring($element.html(), 'b', 4, 8));



//text.textContent = "Hello";
