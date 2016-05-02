window.onload = function(){
	main();
}

function main(){
	'use strict';

	$('.btncl').click(function(){
		window.location.href = "/submitUserId?userid=" + $('.tboxcl').val()
		// $.ajax({
		// 	url: '/submitUserId',
		// 	type: 'GET',
		// 	data: {
		// 		'userid': $('.tboxcl').val()
		// 	},
		// 	success: function(data){
		// 		console.log(data);
		// 	}
		// });
	});
}