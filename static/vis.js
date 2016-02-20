console.log("Making AJAX call")


make an ajax request main.py to start scraping
$.ajax({
   type: 'GET',
    url: '/ajax?keyword=tuxedo&subreddit=TuxedoCats',
    data: {},
    success: function(data){
        console.log(data)
    }
});

console.log("Finishing AJAX call")