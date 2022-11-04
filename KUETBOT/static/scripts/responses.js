function getBotResponse(input) {
    //calls python and gets response
    fetch('/botResponse?a='+ input)
    .then((response) => {
      return response.json();
    })
}