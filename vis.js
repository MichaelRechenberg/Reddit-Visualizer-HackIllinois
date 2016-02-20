function getData() {

    var deferredData = new jQuery.Deferred();

    $.ajax({
        type: "GET",
        url: "/ajax",
        dataType: "json",
        success: function(data) {
            deferredData.resolve(data);
            },
        complete: function(xhr, textStatus) {
            console.log("AJAX Request complete -> ", xhr, " -> ", textStatus);
            }
    });

    return deferredData; // contains the passed data
};


// I used the Deferred structure below because I later added Deferred objects from other asynchronous functions to the `.when`

var dataDeferred = getData();

$.when( dataDeferred  ).done( function( data ) {
    console.log("The data is: " + data);
});