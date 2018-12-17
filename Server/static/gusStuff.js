// //canvas3
// var canvas3 = document.getElementById('canvasgus2');
// var ctx = canvas3.getContext('2d');
// //Variables
// var canvas3x = $(canvas3).offset().left;
// var canvas3y = $(canvas3).offset().top;
// var last_mousex = last_mousey = 0;
// var mousex = mousey = 0;
// var mousedown = false;
// console.log(canvas3x, canvas3y);
// //Mousedown
// $(canvas3).on('mousedown', function(e) {
//     last_mousex = parseInt(e.clientX-canvas3x);
// 	last_mousey = parseInt(e.clientY-canvas3y);
//     mousedown = true;
// });

// //Mouseup
// $(canvas3).on('mouseup', function(e) {
//     mousedown = false;
// });

// //Mousemove
// $(canvas3).on('mousemove', function(e) {
//     mousex = parseInt(e.clientX-canvas3x);
//     mousey = parseInt(e.clientY-canvas3y);

//     if(mousedown) {
//         ctx.clearRect(0,0,canvas3.width,canvas3.height); //clear canvas3
//         ctx.beginPath();
//         var width = mousex-last_mousex;
//         var height = mousey-last_mousey;

// 	cv2.width = imgWidth*0.23;
// 	cv2.height = imgHeight*0.23;
// 	context2.scale(0.23, 0.23);
//         context2.drawImage(img, 0, 0, imgWidth, imgHeight);

//         ctx.rect(last_mousex,last_mousey,width,height);
//         ctx.strokeStyle = 'black';
//         ctx.lineWidth = 2;
//         ctx.stroke();
//     }
//     //Output
//     $('#output').html('current: '+mousex+', '+mousey+'<br/>last: '+last_mousex+', '+last_mousey+'<br/>mousedown: '+mousedown);
// });
