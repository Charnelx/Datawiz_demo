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
				dataType: 'json',
				success: function (data) {

					if (data.empty) {

						error_block.innerHTML = "<strong>No data in selected range.</strong>";
						error_block.style.display = 'block';
					}
					else if (data) {
						var table = $("#records_table").find("tbody");
						var table_inner = $("#records_table").find("tbody>tr");

						for (var i = 0; i < table_inner.length; i++) {
						  	var child = table_inner[i];
						  	if (child.id != 'anchor') {
								child.remove()
                            }
						}

						var trHTML = '';
						var dataLength = data.length;

						for (var i = 0; i < dataLength; i++) {
							var obj = data[i];
							trHTML +=
							'<tr><td>' + data[i].date +
							'</td><td>' + data[i].turnover +
							'</td><td>' + data[i].qty +
							'</td><td>' + data[i].receipts_qty +
							'</td><td>' + data[i].profit +
							'</td></tr>';
						}
						table.append(trHTML);

						alert("Delete this message after testing!");
					}
				},
				error: function(){
					console.log('Error on get_sales data');
				}
			  }) 
			}
