console.log("Entering vis code");
//holds the results of the search (JSON)
var results = null;

//main vis code goes in here, run when the
//  user hits the submit button
//An AJAX call is made, then vis() is called
//  after the success of the call
function search(){

    //construct our query
    var keywords = document.getElementById("keyword").value
    keywords = keywords.split(",");
    console.log(keywords);
    //array containing our resulting query
    query = []
    var derp = 0;
    for(k in keywords){
        if(keywords.hasOwnProperty(k)){
            query.push({name: "keyword" + derp, value: keywords[k]});
            derp++;
        }
    }
    query.push({name:"keywordCount", value:keywords.length});
    var subreddit = document.getElementById("subreddit").value;
    query.push({name:"subreddit", value: subreddit});
    console.log(query);
    console.log($.param(query));

    var surl = '/ajax?keyword=' + keywords + '&subreddit=' + subreddit;
    surl = '/ajax'
    //make an ajax request main.py to start scraping
    //the params sent are:
    //  keywordX : var arg number of keywords
    //  keywordCount : amount of keywords sent
    //  subreddit : the subreddit we want to search
    $.ajax({
       type: 'GET',
        url: surl,
        data: $.param(query),
        success: function(data){
            //the subreddit was invalid, alert the user
            if(data=="InvalidSubreddit"){
                alert("Invalid Subreddit. Try Again")
            }
            //the subreddit was valid, store the results
            //  and have vis() work
            else{
                results = data;
                vis(data);
            }

        }

        //complete: function() {console.log(results)}
    });

}

function vis(){
    for(k in results){
        if(results.hasOwnProperty(k)){
            var str = k + " was found " + results[k] + " time(s).";
            $("#visualizer").append("<p>" + str + "</p>");

        }
    }


}


