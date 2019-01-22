function hasClass(el, className)
{
    if (el.classList)
        return el.classList.contains(className);
    return !!el.className.match(new RegExp('(\\s|^)' + className + '(\\s|$)'));
}

function addClass(el, className)
{
    if (el.classList)
        el.classList.add(className)
    else if (!hasClass(el, className))
        el.className += " " + className;
}

function removeClass(el, className)
{
    if (el.classList)
        el.classList.remove(className)
    else if (hasClass(el, className))
    {
        var reg = new RegExp('(\\s|^)' + className + '(\\s|$)');
        el.className = el.className.replace(reg, ' ');
    }
}

var listagus = [];
var gusObj = {};
var imaginesmexy;
document.getElementById("canvasgus").style.display = 'none';
document.getElementById("part2").style.display = 'none';

//make responsive from JS gusolions
var coloane = document.getElementsByClassName("col-md-6")
for(i=0; i<coloane.length; i++){
	removeClass(coloane[i], 'col-md-4');
	addClass(coloane[i], 'col-md-6');
}


$(document).ready(function () {
	var files = "";
	var image = "";



	$("input[type=file]").click(function () {
		$(this).val("");

	});

	$("input[type=file]").change(function (event) {
		files = this.files;

		indexOfPath = this.files[0].name.split('.').length;
		if (this.files[0].name.split('.')[indexOfPath - 1] === 'pdf') {

			//COD CARE SE VA JUCA CU PDF-UL

		} else {

			// FileReader support
			if (FileReader && files && files.length) {
				var fr = new FileReader();

				fr.onload = function () {
					imaginesmexy = image = fr.result;
					
					document.getElementById("canvasgus").style.display = 'block';
					document.getElementById("uploadImage").style.display = 'none';
					document.getElementById("part2").style.display = 'block';



					cv = document.getElementById("canvasgus");
					context = cv.getContext("2d");

					//draw upload image------------------------------------------->
					var img = new Image();
					img.onload = function () {
						var imgWidth = img.width;
						var imgHeight = img.height;
						cv.width = imgWidth * 0.23;
						cv.height = imgHeight * 0.23;
						context.scale(0.23, 0.23);
						context.drawImage(img, 0, 0, imgWidth, imgHeight);

						//make responsive from JS gusolions
						var coloanex = document.getElementsByClassName("col-md-6")

						while(coloanex.length)
						{
							addClass(coloanex[i], 'col-md-4');
							removeClass(coloanex[i], 'col-md-6');
						}


					}
					img.src = image;

					var context2 = document.getElementById("canvasgus2").getContext("2d");

					//draw image on modifying tool zone ------------------------------------------------------->
					var img2 = new Image();
					img2.onload = function () {
						var imgWidth = img2.width;
						var imgHeight = img2.height;
						cv2 = document.getElementById("canvasgus2");
						cv2.width = imgWidth * 0.23;
						cv2.height = imgHeight * 0.23;
						context2.scale(0.23, 0.23);
						context2.drawImage(img, 0, 0, imgWidth, imgHeight);

						//canvas3
						var canvas3 = document.getElementById('canvasgus2');
						var ctx = canvas3.getContext('2d');

						//Variables
						var canvas3x = $(canvas3).offset().left;
						var canvas3y = $(canvas3).offset().top;
						var last_mousex = last_mousey = 0;
						var mousex = mousey = 0;
						var mousedown = false;

						//console.log(canvas3x, canvas3y);
						//Mousedown
						$(canvas3).on('mousedown', function (e) {
							last_mousex = parseInt(e.clientX - canvas3x);
							last_mousey = parseInt(e.pageY - canvas3y);

							mousedown = true;
						});

						//Mouseup
						$(canvas3).on('mouseup', function (e) {
							mousedown = false;
							listagus.push(gusObj);
						});

						//Mousemove
						$(canvas3).on('mousemove', function (e) {
							mousex = parseInt(e.clientX - canvas3x);
							mousey = parseInt(e.pageY - canvas3y);
							
							// console.log('X ', e.clientX, canvas3x)
							// console.log('Y ',e.pageY, canvas3y)
							/* TINE MINTE SA FACI DIFERENTA DINTRE PUNCTUL LA CARE TE REFERI CAND CALCULEZI DISTANTE
								PAGEY FACE REFERITOR LA PAGINA, CLIENTY REFERITOR LA VIEWPORT, SI MAI AI SI REFERITOR LA MONITORU FIZIC,
								DAR NU AI NEVOIE.

								DACA O SA VREI RESPONSIVE PE LATIME, SA BAGI SI PE X.
								*/
							ctx.fillRect(e.clientX,e.pageY,1,1);
							ctx.stroke();
							//console.log(mousex,mousey, last_mousex, last_mousey);

							if (mousedown) {
								ctx.clearRect(0, 0, canvas3.width / 23 * 100, canvas3.height / 23 * 100); //clear canvas3
	

								ctx.beginPath();
								var width = mousex - last_mousex;
								var height = mousey - last_mousey;
								// console.log(mousey,'   ', last_mousey)

								cv2.width = imgWidth * 0.23;
								cv2.height = imgHeight * 0.23;
								context2.scale(0.23, 0.23);
								context2.drawImage(img, 0, 0, imgWidth, imgHeight);


								for (var index = 0; index < listagus.length; index++) {

									ctx.rect(listagus[index].last_m_x / 23 * 100,
										listagus[index].last_m_y / 23 * 100,
										listagus[index].gaz / 23 * 100,
										listagus[index].heightx / 23 * 100);

									
								ctx.strokeStyle = 'black';
								ctx.lineWidth = 2;
								ctx.stroke();

									//ASTA TRIMIT PE SERVER, AICEA SUNT COORDONATELE, PRESTO!!! CRESCENDO!!!

									console.log(index, '<== index,coord ==>', listagus[index].last_m_x / 23 * 100,
										listagus[index].last_m_y / 23 * 100,
										(listagus[index].gaz + listagus[index].last_m_x) / 23 * 100,
										(listagus[index].heightx + listagus[index].last_m_y) / 23 * 100);

								}

								ctx.rect(last_mousex / 23 * 100, last_mousey / 23 * 100, width / 23 * 100, height / 23 * 100);
								gusObj = {
									'last_m_x': last_mousex,
									'last_m_y': last_mousey,
									'gaz': width,
									'heightx': height,
								};

								ctx.strokeStyle = 'black';
								ctx.lineWidth = 2;
								ctx.stroke();
							}
							//Output
							$('#output').html('current: ' + mousex + ', ' + mousey + '<br/>last: ' + last_mousex + ', ' + last_mousey + '<br/>mousedown: ' + mousedown);
						});
					}
					img2.src = image;

					//canvas gus spaghetti
					showUploadButton();
				}

				fr.readAsDataURL(files[0]);
			}
		}


	});

	//
	$('#uploadForm').on('submit', function (event) {
        event.preventDefault();
        
        for (var index = 0; index < listagus.length; index++) {
            listagus[index].last_m_x = Math.round(listagus[index].last_m_x / 23 * 100);
            listagus[index].last_m_y = Math.round(listagus[index].last_m_y / 23 * 100);
            listagus[index].gaz = Math.round(listagus[index].gaz / 23 * 100);
            listagus[index].heightx = Math.round(listagus[index].heightx / 23 * 100);
        }

		var formData = new FormData();
		formData.append("file", imaginesmexy);
		console.log(JSON.stringify(listagus))
		coord = JSON.stringify(listagus).replace(/{/g, '(').replace(/}/g, ')').replace(/((,[^,]*){3})(,)/g, '$1\\');
		console.log(coord);

		formData.append("coordinates", coord);

		var request = $.ajax({
			url: "/serveste-mi-cererea",
			data: formData,
			cache: false,
			contentType: false,
			processData: false,
			method: 'POST',
			type: 'POST',
			//contentType
		});

		request.done(function (msg) {
			$("#log").html(msg);
			console.log(msg);
			$( "#gusPlaceHolderResponseImage" )[0].hidden = true;
			$( "#gusResponseFromServer" )[0].hidden = false;
			$( "#gusResponseFromServerParagraph" )[0].innerHTML = msg;
		});

		request.fail(function (jqXHR, textStatus) {
			alert("Request failed: " + textStatus);
		});
	});

	$('#uploadSpot').click(function () {
		$("input[type=file]").trigger('click');
	});
});


function showUploadButton() {
	var $uploadButton = $('#uploadButton');

	$uploadButton.show();
	$uploadButton.addClass('elementToFadeInAndOut');
}









