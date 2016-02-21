console.log("Entering vis code");
//holds the results of the search (JSON)
var results = null;

//main vis code goes in here, run when the
//  user hits the submit button
//An AJAX call is made, then vis() is called
//  after the success of the call
function search(){

    //construct our JSON
    var keywords = document.getElementById("keyword").value
    keywords = keywords.split(",");
    query = {
        'keywords': [],
        'subreddits': []
    };
    var derp = 0;
    for(k in keywords){
        if(keywords.hasOwnProperty(k)){
            query['keywords'].push(keywords[k]);
            derp++;
        }
    }
    var subreddits = document.getElementById("subreddit").value;
    subreddits = subreddits.split(",");
    derp = 0;
    for(k in subreddits){
        if(subreddits.hasOwnProperty(k)){
            query['subreddits'].push(subreddits[k]);
            derp++;
        }
    }
    console.log(query);
    console.log(JSON.stringify(query));
    //make an ajax request main.py to start scraping
    $.ajax({
       type: 'POST',
        url: '/ajax',
        data: JSON.stringify(query),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
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

        },
        error: function(data){
            alert("Error");
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
    words = []
    for(k in results){
        if(results.hasOwnProperty(k)){
            str = "";
            numOfWords = results[k];
            for(x = 0; x < numOfWords; x++){
                str+= (k + ' ');
            }
            words.push(str);

        }
    }
    console.log(words);

}

