function	dateRangeChangeAJAX() { 
			var element = document.getElementById('drp_autogen0');
			var txt = element.textContent || element.innerText;
			var error_block = document.getElementById('error_msg');
			error_block.style.display = 'none';
			
			$.ajax({
				type: 'post',
				url: '/general/',
				data: {
				  'info': txt
				},
				dataType: 'html',
				success: function (data) {
					if (data) {
						var container = $("#records_block");
						container.contents().remove();

						container.append(data)
						// console.log(data)
					}
					else {
						error_block.innerHTML = "<strong>No data in selected range.</strong>";
						error_block.style.display = 'block';
					}
				},
				error: function(){
					console.log('Error on get_sales data');
				}
			  }) 
			}
