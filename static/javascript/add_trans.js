$(document).ready(function() {
	var checked; 
	$('#id_include_me').click(function() {
		checked = $('#id_include_me').is(':checked'); 
		console.log(checked); 
		
		if (checked == true) {
			$('#submitbutton').val('Next'); 
		}
	})


});

	




