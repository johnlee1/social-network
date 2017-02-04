$(document).ready( function() { $(".commentInput").on("click", ".commentBtn", addComment )} );


window.setInterval(function () {
    $.ajax({
        type: "GET",
        url: "/socialnetwork/refreshGlobal/",
        datatype: "json",

        success: function(response){
            posts = response[0]; 
            $(posts).each(function() {
                var post = $(this)[0].fields
                var username = $(this)[0].fields.username
                var authorId = $(this)[0].fields.userId
                var $outsideDiv1 = $("<div>", {class: "panel panel-default"});
                var $outsideDiv2 = $("<div>", {class: "col-md-6 col-md-offset-3"});
                var $outsideDiv3 = $("<div>", {class: "media"});
                var $outsideDiv4 = $("<div>", {class: "panel-body post"});
                var $newDiv = $("<div>", {class: "panel-heading"});
                var $newImg = $("<img>", {src: "/photo/"+authorId, class: "img-circle", width: "50", height: "50"});
                var $newLink = $("<a>", {href: "/"+username+"/"});
                $newLink.text(post.username);
                var $newP = $("<p>", {class: "pull-right"});
                $newP.text(post.time + " | " + post.date)
                $newDiv.append($newImg);
                $newDiv.append($newLink);
                $newDiv.append($newP);
                var $otherDiv = $("<div>", {class: "panel-body"});
                $otherDiv.text(post.content);
                $outsideDiv1.append($newDiv);
                $outsideDiv1.append($otherDiv);
                $outsideDiv2.append($outsideDiv1);
                $outsideDiv3.append($outsideDiv2);
                $outsideDiv4.append($outsideDiv3);
                $(".timelineBegin").prepend($outsideDiv4);
            });
        },

        error: function(response){
            return false;
        },
    });
}, 5000);


function getFormattedDate(dateString){
    var theDate = new Date(dateString);
    finalDateString = "";
    monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    finalDateString = finalDateString.concat(monthNames[theDate.getMonth()] + ". ");
    finalDateString = finalDateString.concat(theDate.getDate() + ", ");
    finalDateString = finalDateString.concat(theDate.getUTCFullYear() + ", ");
    finalDateString = finalDateString.concat(theDate.getUTCHours()%12 + ":");
    finalDateString = finalDateString.concat(theDate.getUTCMinutes() + " ");
    if(theDate.getUTCHours() > 12){
        finalDateString = finalDateString.concat("p.m.");
    }else{
        finalDateString = finalDateString.concat("a.m.");
    }
    
    return finalDateString;
}


function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        }
    }
    return "unknown";
}


function addComment() {

    var comment = $(this).closest(".commentInput").find("textarea[name=body]").val();
    var commentsThread = $(this).closest(".commentSection").find(".commentsThread");
    var postId = $(this).closest(".postContainer").attr("postId");

    var csrfToken = getCSRFToken();

    $.ajax({
        type: "POST",
        url: "/addComment/",
        data: { body : comment,
                post_id : postId,
                csrfmiddlewaretoken : csrfToken },
        datatype: "json",

        success: function(response){
            publishComment(response);
            return false;
        },

        error: function(response){
            return false;
        },
    });
}

function publishComment(response) {
    var postId = response[0].fields.post;
    var comment = response[0].fields.body;
    var datetime = response[0].fields.datetime;
    var username = response[1].fields.username;
    var authorId = response[2].pk;

    date = getFormattedDate(datetime);

    var post = $(".feed-container").find("[postId=" + postId + "]");
    $(post).find(".commentInput").find("textarea[name=body]").val("");

    var commentSection = $(post).find(".commentSection");

    var $newComment = $("<div>", {class: "panel-footer"});
    var $panelHeader = $("<div>", {class: "panel-heading"});
    var $newImg = $("<img>", {src: "/photo/"+authorId, class: "img-rounded", width: "40", height: "40"});
    var $newLink = $("<a>", {href: "/"+username+"/"});
    var $newP = $("<p>", {class: "pull-right"});
    
    $newLink.text(username);
    $newP.text(date);
    $panelHeader.append($newImg);
    $panelHeader.append($newLink)
    $panelHeader.append($newP);
    $newComment.append($panelHeader);
    $newComment.append(comment);

    $($newComment).hide();
    $($newComment).insertBefore( $(commentSection).children().last() );
    $($newComment).slideDown();
    return;
}

