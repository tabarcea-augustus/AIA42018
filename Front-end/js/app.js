$(document).ready(function(){
	var files = "";
	var image = "";

    $("input[type=file]").click(function(){
        $(this).val("");
    });

    $("input[type=file]").change(function(event){
        files = this.files;

        // FileReader support
	    if (FileReader && files && files.length) {
	        var fr = new FileReader();

	        fr.onload = function () {
	        	image = fr.result;

	            document.getElementById('uploadImage').src = image;

	            showUploadButton();
	        }

	        fr.readAsDataURL(files[0]);
	    }
    });

    //
    $('#uploadForm').on('submit', function(event){
    	event.preventDefault();

		var request = $.ajax({
		  url: "/",
		  type: "POST",
		  data: {
		  	image : image,
		  },
		  dataType: "json"
		});

		request.done(function(msg) {
		  $("#log").html( msg );
		});

		request.fail(function(jqXHR, textStatus) {
		  alert( "Request failed: " + textStatus );
		});
    });

    $('#uploadSpot').click(function(){
    	$("input[type=file]").trigger('click');
    });
});


function showUploadButton(){
	var $uploadButton = $('#uploadButton');

	$uploadButton.show();
	$uploadButton.addClass('elementToFadeInAndOut');
}

