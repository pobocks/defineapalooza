/* Extremely basic SPA (single page application) functionality */
$(function () {
    $('#word-form').on('click submit', 'button[type="submit"]',
		       function (e){
			   e.preventDefault();
			   e.stopPropagation();
			   var word = $("#word").val();
			   $.ajax({url:"/api/v1/word/" + word,
				   headers:{accept: "text/html"},
				   dataType:'html'})
			       .done(function (data) {
				       $('#definition-content').html(data);
				       document.title = "Results for: " + word;
				   })
			       .fail(function (data) {

				   $("#definition-content").html(
				       "<p>No result found, or an error occurred.</p>");
				   document.title = "No results for: " + word;
			       });			   
		       });
});
