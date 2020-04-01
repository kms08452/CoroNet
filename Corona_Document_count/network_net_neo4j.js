/************
 * 전역변수 모음
 ************/
var svg; //캔버스 그려주기


var color = colors_closer(); //색상
var imgData; //mol image 변수

var tooltip_info = tooltip_text_img_closer(); //마우스 오버시 툴팁
var fix_tooltip_info = fix_tooltip_closer(); //고정용 툴팁
var fixed_tooltip_util = fixed_tooltip_util_closer(); //고정용 툴팁에 필요한 유틸들
var fixed_tooltip_array= []; //고정된 tooltip은 여기에 담아
var arrow_pool = []; //생성 화살표들 담아 놓음
var fixed_tooltip_unique = []; //중복 아이디 확인을 위해서
var pdb_obj = {}; //pdb 객체 담기
var arrow_line = null; //툴팁 화살표

var node_stop_val; //노드 움직임 멈춤

var nodes; //노드 데이터
var links; //링크 데이터
var radius = 7; //노드 크기

var availableTags = []; //검색어 자동완성만들기 변수
var nodeName;


//네트워크 뷰 만들어주는 메인
function network_view(netData){

	//뷰 화면 만들기
	function view(){

		var rootID = netData.nodes[0].nid;

		var m = [20, 120, 20, 120],
			w = 948 - m[1] - m[3],
			h = 600 - m[0] - m[2];

		svg = d3.select("#network").append("svg")
			.attr("width", w + m[1] + m[3])
			.attr("height", h + m[0] + m[2]);

		const forceX = d3.forceX(w / 2 + m[1]).strength(0.003);
		const forceY = d3.forceY(h / 2 + m[0]).strength(0.003); //0.003
		var simulation = d3.forceSimulation()
			.force("link", d3.forceLink().distance(300).strength(0.002).id(function(d) { return d.nid; }))
			.force("x", forceX)
			.force("y", forceY)
			.force("charge", d3.forceManyBody())
			.force("center", d3.forceCenter(w / 2 + m[1], h / 2 + m[0]));

		simulation.nodes(netData.nodes).on("tick", ticked).stop();
		simulation.force("link").links(netData.links);
		simulation.restart();

		var g = svg.append("g").attr("class", "node_container");


		/**************
		 *
		 * 마우스 오버시 툴팁
		 *
		 **************/
		var tool_tip = d3
			.tip()
			.attr("class", "d3-tip")
			.attr("width", "230px")
			.offset(function(d){
				return [0, 0]
			})
			.direction(function(d){
				//console.log(d.x + ", " + d.y)
				//console.log(w + ", " + h)
				/* 	if(d.x > w && d.y > h-130){
                            return "nw";
                           }else if(d.x > w){
                            return "w";
                        }else if(d.y > h-130){
                            return "ne";
                        }else{
                            return "se";
                        }   */
				return "e";
			})
			.html(function(d){
				console.log(d)
				if(d.site != "" && d.site != null){ //binding site 정보가 있을 경우
					return "<div id='wrap-tip'><strong style='font-weight:bold; font-size:13px;'>" + tooltip_info.getText(d) + "</strong>" + "<span>  ["+d.site +"]</span>" + "<br>" + tooltip_info.imageToolTip(d)+"</div>";

				}else if(d.mdl != null) { //이미지 있을 경우
					return "<div id='wrap-tip'><strong style='font-weight:bold; font-size:13px;'>" + tooltip_info.getText(d) + "</strong>" + "<br>" + tooltip_info.imageToolTip(d)+"</div>";

				} else if(d.pmdl != null){
					return "<div id='wrap-tip'><strong style='font-weight:bold; font-size:13px;'>" + tooltip_info.getText(d) + "</strong>" + "<br>" + tooltip_info.pdb_imageToolTip(d.pmdl)+"</div>";

				} else if(d.tdesc != null && d.tdesc.length > 0){ //타겟의 description 이 있을 경우
					return "<div id='wrap-tip'><strong style='font-weight:bold; font-size:13px;'>" + tooltip_info.getText(d) + "</strong>" + "<br>" + "<div id='target_description' style='position:absolute; background-color:#FFFFFF; border:1px solid rgba(255, 91, 95, 0.7); box-shadow: 5px 5px 5px 3px gray; border-radius:0 3px 3px 3px; margin-top:5px; margin-left:-5px; padding:5px 5px 5px 5px; width:230px; font-color:black; '>" +tooltip_info.target_detail(d) + "</div></div>";

				}else if(d.phase != null){ //임상정보의 임상단계가 있는 경우
					return "<div id='wrap-tip'><strong style='font-weight:bold; font-size:13px;'>" + tooltip_info.getText(d) + "</strong>" + "<br>" + "<div id='target_description' style='position:absolute; background-color:#FFFFFF; border:1px solid rgba(255, 91, 95, 0.7); box-shadow: 5px 5px 5px 3px gray; border-radius:0 3px 3px 3px; margin-top:5px; margin-left:-5px; padding:5px 5px 5px 5px; width:230px; font-color:black; '>" +tooltip_info.ct_title(d) + "<br>&nbsp; - " + tooltip_info.ct_phase(d)+"</div></div>";

				}else{ //기타
					return "<div id='wrap-tip'><strong style='font-weight:bold; font-size:13px;'>" + tooltip_info.getText(d) + "</strong>" + "</div>";

				}
			})

		svg.call(tool_tip)

		/*****************/
		var sizeScale = d3.scaleLinear()
			.domain([0, d3.max(netData.links.map(function(d){return d.cnt}))])
			.range([2,10]);
		links = g.append("g")
			.attr("class", "net_link")
			.selectAll("line")
			.data(netData.links)
			.enter().append("line")
			.attr("stroke-opacity", "0.7")
			.attr("stroke-width", function(l){
				return sizeScale(l.cnt)
			})
			.attr("stroke", function(l){
				return color.link_palette(l.group);
			});

		var t = d3.zoomTransform(self.svg.node()); //node의 내부 transform 정보 = 화살표 거리와 각도 계산을 위하여

		nodes = g.append("g")
			.attr("class", "net_node")
			.selectAll("circle")
			.data(netData.nodes)
			// .enter().append("svg:image")
			// .attr("xlink:href", "https://image.flaticon.com/icons/svg/261/261043.svg")
			// .attr("width", 30)
			// .attr("height",30)
			// .attr("x", function (d) {return -15})
			// .attr("y", function (d) {return  -15})
			//2020-01-13 mskim
			.enter().append("circle")
			.attr("r", 15)
			.attr("fill", function(d) {
			 	//console.log(d.group);
			 	return color.palette(d.group);
			})
			// .append("text")
			// .attr("dx", 12)
			// .attr("dy", ".35em")
			// .text(function(d) { return d.nm ? d.nm : d.cid	 })
			.attr("id", function(d, i){
				//검색어 자동완성을 위해서
				var names = d.nm ? d.nm : d.cid ? d.cid : d.smiles;
				availableTags.push(names);
				return names;

			})
			.call(d3.drag()
				.on("start", dragstarted)
				.on("drag", dragged)
				.on("end", dragended)
			)
			.style("cursor", "pointer")
			.on("click", function(d, i){
				fix_tooltip_info.clickTooltip(d, i);
			})
			.on("mouseover", tool_tip.show)
			.on("mouseout", function(d){
				tool_tip.hide(d);
			})
			.on("dblclick", function(d) { alert( tooltip_info.getText(d)); })


		var textLabel = g.append("g")
			.attr("class", "labels")
			.selectAll("g")
			.data(netData.nodes)
			.enter().append("g")
			.on("click", function(d){

				d3.select(this).text(function(d){
					return null;
				});
			});




		/*********
		 *
		 * 노드 움직임 관련 모음
		 *
		 **********/
		function ticked() {

			links
				.attr("x1", function(d) {
					return d.source.nid == rootID ? d.source.x + (w / 2 + m[1] - d.source.x) * 0.01 : d.source.x;
				})
				.attr("y1", function(d) {
					return d.source.nid == rootID ? d.source.y + (h / 2 + m[0] - d.source.y) * 0.01 : d.source.y;

				})
				.attr("x2", function(d) {
					return d.target.nid == rootID ? d.target.x + (w / 2 + m[1] - d.target.x) * 0.01 : d.target.x;

				})
				.attr("y2", function(d) {
					return d.target.nid == rootID ? d.target.y + (h / 2 + m[0] -7 - d.target.y) * 0.01 : d.target.y;

				});

			nodes
				.attr("cx", function(d, i) {
					return d.nid == rootID ? d.x + (w / 2 + m[1] - d.x) * 0.01 : d.x;

				})
				.attr("cy", function(d) {
					return d.nid == rootID ? d.y + (h / 2 + m[0] - d.y) * 0.01 : d.y;

				});

			textLabel.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
		}

		function dragstarted(d) {
			if (!d3.event.active) simulation.alphaTarget(0.3).restart();
			d.fx = d.x;
			d.fy = d.y;
		}

		function dragged(d) {
			removeTooltip();
			d.fx = d3.event.x;
			d.fy = d3.event.y;
		}

		function dragended(d) {
			if (!d3.event.active) simulation.alphaTarget(0);
			//node 멈춤 기능 상태로 드래그 하기.
			if(node_stop_val == "Node Moving"){
				d.fx =  d3.event.x;
				d.fy =  d3.event.y;
			}else{
				d.fx = null;
				d.fy = null;
			}
		}

		d3.select(".node_stop_btn").on("click",function(){
			node_stop_val = $(".node_stop_btn").attr("value");

			if(node_stop_val=="Node Moving"){
				d3.select(this).attr("value","Node Stop");
				nodes.each(function(d){
					d.fx = d.x;
					d.fy = d.y;
				})
			}else{
				d3.select(this).attr("value","Node Moving");
				nodes.each(function(d){
					d.fx = null;
					d.fy = null;
				})
			}//if
		});
		/**********************/



		var zoom_handler = d3.zoom()
			.on("zoom", zoom_actions);

		zoom_handler(svg);

		function zoom_actions(){
			g.attr("transform", d3.event.transform)

			//화살표 위치 전달
			nodes.each(function(d, i){
				arrow(d, i, arrow_line);
			})

		}

		//초기화버튼
		function resetted(){

			if(confirm("Do you want to reset?")){
				g.selectAll("text").text(function(d){
					return null;
				})
				svg.transition()
					.duration(750)
					.call(zoom_handler.transform, d3.zoomIdentity);

				d3.selectAll('input').property('checked', true);
				nodes.style("visibility", "visible");
				links.style("visibility", "visible");
			}
		}

		/*****************************
		 *
		 *
		 * 범례 지정
		 *
		 *
		 ****************************/
		var legends = [{"legend":"Query","group":1},{"legend":"Chemicals","group":2},{"legend":"Drug Compounds","group":3},{"legend":"Chemiverse Compounds","group":4},{"legend":"Targets","group":5},{"legend":"Disease","group":6},{"legend":"Protein Structure","group":7},{"legend":"Ligand Structure","group":8},{"legend":"Clinical Trials","group":9}];
		var legends_test = [{1:"Query"},{2:"Chemicals"},{3:"Disease"},{4:"Mutation"},{5:"Gene"},{6:"Species"},{7:"CellLine"},{8:"Hallmark"},{9:"Clinical Trials"}];
		var legends_test2 = ["Query","Chemicals","Disease","Mutation","Gene","Species","CellLine","Hallmark","Clinical Trials"];

		legendFilter();

		function legendFilter(){
			d3.select(".legend-filter")
				.selectAll("div")
				.data(legends)
				.enter()
				.append("div")
				.attr("class", "checkbox-container")
				.append("label")
				.each(function(d){
					d3.select(this).append("input")
						.attr("type", "checkbox")
						.attr("id", function(d){
							//console.log("범례 아이디 : chk_"+d.group);
							return "chk_"+d.group;
						})
						.attr("checked", true)
						.on("click", function(d, r){
							var link_Visibility = this.checked ? "visible" : "hidden";

							nodes.each(function(e, i){
								filterGraph(e, d, link_Visibility, r);
							}); //nodes
						})

					d3.select(this).append("span")
						.text(function(d, i){
							return legends_test2[d.group-1]
							var lf = legends.filter(function(legends){ //legend label 뽑아오고
								return legends.group == d.group;
							});

							return lf[0].legend;
						})
						.style("color", function(d){return color.palette(d.group)})
				});
			$("#legend-sidebar").show();
		}


		function filterGraph(e_node, d_node, link_Visibility, r){

			//(1). hidden된 범례들의 노드와 링크도 hidden 처리
			if(e_node.group === d_node.group){
				if(link_Visibility === "hidden"){
					links.style("visibility", function(o){
						var link_OriginalVisibility = $(this).css("visibility");
						return (o.target == e_node || o.source == e_node) ? link_Visibility : link_OriginalVisibility;
					});

					nodes.style("visibility", function(o){
						var node_OriginalVisibility = $(this).css("visibility");
						return (o.group == e_node.group) ? link_Visibility : node_OriginalVisibility;

					});
				}//if
			}//if




			if(link_Visibility === "visible"){
				//node visible 처리
				if(e_node.group === d_node.group){
					nodes.style("visibility", function(o){
						var node_OriginalVisibility = $(this).css("visibility");

						return (o.group == e_node.group) ? link_Visibility : node_OriginalVisibility;
					})
				}

				//범례가 check된 group들의 link상태를 고려하진 않고 체크되지 않은 노드들의 link를 계속 hidden 시켜놓는데에 초점을 맞춤.
				links.style("visibility", function(o){
					var link_OriginalVisibility = $(this).css("visibility");

					if(e_node.group != 1){ //query는 제외하고

						if($("#chk_"+e_node.group).is(":checked")){
							return true;//if문 빠져나가는 용도로 true 적용;
						}else if(!$("#chk_"+e_node.group).is(":checked")){ //체크되지 않은 그룹 중에

							if(o.source === e_node || o.target === e_node){ //체크되지 않은 node의 edge 확인해서 계속 hidden처리
								return "hidden";
							}else{	//나머진 상태 유지
								return link_OriginalVisibility;
							}

						}

					}//if

					//결국 check 되어있는 노드들끼리 연결, d3.js에선 아래처럼 return 으로 안해줘도 default 값으로 넣음.
					return link_Visibility;
				})//links

			}
		}

		$("#chk_1").remove();

		//링크 범례
		var link_legend = [{"legend":"Direct-Connection","group":1}, {"legend":"Open_Suggestion","group":2}, {"legend":"Close_Relation","group":3}, {"legend":"Neigbor_Relation","group":4}]
		d3.select(".link-legend")
			.selectAll("div")
			.data(link_legend)
			.enter()
			.append("div")
			.attr("class", "link-container")
			.append("label")
			.style("color", function(l){ return color.link_palette(l.group)})
			.text(function(d, i){
				console.log(d)
				return "●ㅡ " + "  "+d.legend;
			})

		/************************************/


		/*************
		 *
		 *
		 * 검색어기능
		 *
		 ************/
		$('.searchNode').on('click', function(){
			search_node();
		})

		function search_node(){
			nodeName = $('#nodes_search').val();
			var theNode = d3.select("[id='"+nodeName +"']");

			textLabel.append("text")
				.attr("x", 14)
				.attr("y", ".31em")
				.style("font-family", "sans-serif")
				.style("font-size", "1.2em")
				.text(function(d){
					if(nodeName == ""){
						return null;
					}
					if(tooltip_info.getText(d).indexOf(nodeName) !== -1){
						return tooltip_info.getText(d);
					}
				})
		}

		var $_searchNodes = $('#nodes_search');

		$.ui.autocomplete.prototype._renderItem = function(ul, item){
			var re = new RegExp($.trim(this.term.toLowerCase()));
			var t = item.label.replace(re, "<span style='font-weight:600; color:#5c5c5c;'>" + $.trim(this.term.toLowerCase()) + "</span>");

			return $("<li></li>")
				.data("item.autocomplete", item)
				.append("<a>" + t + "</a>")
				.appendTo(ul);
		}

		//검색기능 함수들
		$_searchNodes.autocomplete({
			source: availableTags
		});


		/******************
		 *
		 * 기타함수 모음
		 *
		 ***************/

		//선택버튼 이벤트 함수
		select_event_setting();
		function select_event_setting(){

			/*nodes.on('click', function(d, i){ //d3.v4 에서 click bug 때문에 따로 설정
				fix_tooltip_info.clickTooltip(d, i);
			}) */

			//리셋버튼
			d3.select(".node_reset_btn")
				.on("click", resetted);

		}



	}

	return function(){
		view()
	}


}

//고정용 툴팁 생성용
function fix_tooltip_closer(){
	console.log('생성');
	return {
		clickTooltip : function(d, i){
			$('#fixed_tooltip').show();

			var boxline = 'boxline_'+i //화살표를 위한 상자
			var draggable = 'draggable_'+i;
			var arrow_fix = 'arrow_fix_'+i; //화살표 고정 아이콘
			var resize = 'resize_'+i;

			fixed_tooltip_array.push(boxline);

			$.each(fixed_tooltip_array, function(index, el){
				if($.inArray(el, fixed_tooltip_unique) == -1){

					fixed_tooltip_unique.push(el);
					fixed_tooltip_util.fixed_tooltip_open(boxline, draggable, arrow_fix, resize, d, i);

					fixed_tooltip_draggable(boxline, draggable, resize);
				}
			});
		},

	}
}


//고정용 툴팁 생성에 필요한 유틸들
function fixed_tooltip_util_closer(){

	//고정용 이미지 불러오기
	function imageData_self(d, i){
		molecule_img(d.mdl);

		if(imgData != null){
			$('#fixed_mol_'+i).attr("src", imgData);
		}else if(imgData == null){
			$('#fixed_mol_'+i).attr("src", "../../img/common/no_img.jpg");
		}
	}

	//고정용 단백질 이미지 불러오기
	function pdb_imgData_self(pmdl, i){
		pdb_img(pmdl, i);

		if(imgData != null){
			$('#fixed_mol_'+i).attr("src", imgData);
		}else if(imgData == null){
			$('#fixed_mol_'+i).attr("src", "../../img/common/no_img.jpg");
		}
	}

	//툴팁 화살표 만들기
	function make_arrow(d, i, boxline){

		var arrow_containers = "arrow_container_"+i;
		arrow_line = "arrow_line_"+i;

		$('#'+boxline).append("<div class='arrow_line'></div>");
		$('.arrow_line').attr("class", arrow_line).attr('id', 'arrow_line');
		$('.'+arrow_line).css({
			"position":"absolute",
			"width":"1px",
			"background-color":"black",
			"z-index":"100",
			"opacity":"0.5",
			"-webkit-transform-origin": "top left",
			"-moz-transform-origin": "top left",
			"-o-transform-origin": "top left",
			"-ms-transform-origin": "top left",
			"transform-origin": "top left",
		})

		arrow_pool.push(arrow_line);
		arrow(d, i, arrow_line);
	}



	return {
		fixed_tooltip_open : function(boxline, draggable, arrow_fix, resize, d, i){

			var t = d3.zoomTransform(self.svg.node())
			var x = d.x*t.k+20+t.x;
			var y = d.y*t.k+310+t.y;

			$('#fixed_tooltip').append("<div id='boxline_' class='boxline_tip'><div>");
			$('#boxline_').attr('id', boxline);
			$('#'+boxline).css('height', 0);

			$('#'+boxline).append("<div id='draggable_' class='ui-widget-content' style='cursor:move;'></div>");
			$('#draggable_').attr('id', draggable);

			$('#'+draggable).append("<div id='arrow_fix_' style='width:100%; height:100%; overflow:hidden;'></div>");
			$('#arrow_fix_').attr('id', arrow_fix);

			$('#'+arrow_fix).append("<div id='resize_'></div>");
			$('#resize_').attr('id', resize);

			$("#"+draggable).append("<div id='arrow_fix_icon_'></div>");
			$("#arrow_fix_icon_").attr("id", "arrow_fix_icon_"+i);

			$('#'+draggable).css({
				'top':y,
				'left':x,
			})

			if(d.site != "" && d.site != null){
				$('#'+draggable).css({"width":"220px", "height":"auto", "z-index":"2", "opacity":"0.9", "position":"absolute"});
				$("#"+resize).html("<strong style='font-weight:bold; font-size:13px; margin:3px;'>" +tooltip_info.getText(d) + "</strong></br>" + "<span> [" + d.site +"]</span>" + "<br>" + "<img id='fixed_mol_' src='../../img/common/none.png' style='background-color:white; opacity:0.9; width:100%; height:100%; position:upset; margin-top:2px;'>");
				$("#fixed_mol_").attr("id", "fixed_mol_"+i);
				imageData_self(d, i);

			} else if(d.mdl != null) {

				$('#'+draggable).css({"width":"220px", "height":"auto", "z-index":"2", "opacity":"0.9", "position":"absolute"});
				$("#"+resize).html("<strong style='font-weight:bold; font-size:13px; margin:3px;'>" +tooltip_info.getText(d) + "</strong>" + "<br>" + "<img id='fixed_mol_' src='../../img/common/none.png' style='background-color:white; opacity:0.9; width:100%; height:100%; position:upset; margin-top:2px;'>");
				$("#fixed_mol_").attr("id", "fixed_mol_"+i);
				imageData_self(d, i);

			} else if(d.pmdl != null){
				$('#'+draggable).css({"width":"220px", "height":"auto", "z-index":"2", "opacity":"0.9", "position":"absolute"});
				$("#"+resize).html("<strong class='pdb_full_name' style='font-weight:bold; font-size:13px; margin:3px;'>" +tooltip_info.getText(d) + "</strong>" +"<a class='ngl_search' id='ngl_search_' style='float:right; color:blue; text-decoration:underling;'>3D VIEW</a>"+ "<br>" + "<img id='fixed_mol_' src='../../img/common/none.png' style='background-color:white; opacity:0.9; width:100%; height:100%; position:upset; margin-top:2px;'>");
				$("#fixed_mol_").attr("id", "fixed_mol_"+i);
				$("#ngl_search_").attr("id", "ngl_search_"+i);

				if(d.pmdl != null){	pdb_obj["ngl_search_"+i]= tooltip_info.getText(d); } //ngl 검색을 위해서 pdb만 map 형성

				pdb_imgData_self(d.pmdl, i);

			} else if(d.tdesc != null && d.tdesc.length > 0){
				$("#"+draggable).css({"width":"220px", "height":"auto", "z-index":"2", "opacity":"0.9", "top": y, "position": "absolute"})
				$("#"+resize).html("<strong style='font-weight:bold; font-size:13px; margin:3px;'>" +tooltip_info.getText(d) + "</strong>" + "<br>" + "<div id='target_description' style='margin-top:5px; padding:5px 5px 5px 5px; font-color:black;'>" +tooltip_info.target_detail(d) + "</div>");
			} else if(d.phase != null){ //임상정보의 임상단계가 있는 경우
				$("#"+draggable).css({"width":"220px", "height":"auto", "z-index":"2", "opacity":"0.9", "top": y, "position": "absolute"})
				$("#"+resize).html("<strong style='font-weight:bold; font-size:13px; margin:3px;'>" + tooltip_info.getText(d) + "</strong>" + "<br>" + "<div id='target_description' style='margin-top:5px; padding:5px 5px 5px 5px; font-color:black;'>" +tooltip_info.ct_title(d) + "<br>&nbsp; - " + tooltip_info.ct_phase(d)+"</div>");

			}else{
				$("#"+draggable).css({"width":"220px", "height":"auto", "z-index":"2", "opacity":"0.9", "top": y, "position":"absolute"});
				$("#"+resize).html("<strong style='font-weight:bold; font-size:13px; margin:3px;'>" +tooltip_info.getText(d) + "</strong>" + "<br>" + "<div id='target_description' style='visibility:hidden;'><br></div>");
				//$("#"+resize).html("<strong style='font-weight:bold; font-size:13px; margin:3px;'>" +tooltip_info.getText(d) + "</strong>" + "<br>" + "<div id='target_description' style='visibility:hidden;'>" +tooltip_info.target_detail(d) + "</div>");

			}

			make_arrow(d, i, boxline);
		},
	}

}

//툴팁 이동 및 리사이즈
function fixed_tooltip_draggable(boxline, draggable, resize){
	//console.log("고정용 툴팁 - 선택된 툴팁"+ draggable)

	$('.ui-widget-content').draggable({

		drag:function(){

			nodes.each(function(d, i){
				arrow(d, i);
			})

		}

	});
	$('#'+draggable).resizable({
		start: function(e, ui){
			$('#'+resize).css("width", $(this).outerWidth()-5).css("height", $(this).outerHeight()-25);
		},
		resize: function(e, ui){
			$('#'+resize).css("width", $(this).outerWidth()-5).css("height", $(this).outerHeight()-25);
			nodes.each(function(d, i){
				arrow(d, i)
			})
		},
		stop: function(e, ui){
			$('#'+resize).css("width", $(this).outerWidth()-5).css("height", $(this).outerHeight()-25);
		}
	})
}


//툴팁을 위한 텍스트와 이미지 생성 함수
function tooltip_text_img_closer(){

	return {
		getText : function(d){
			var query_name;

			if(d.group == 1){
				query_name = "Query";
			}else if(d.group != 1){
				query_name = d.smiles;
			}

			return d.nm ? d.nm : d.cid ? d.cid : query_name;
		},

		target_detail : function(d){ //타겟 설명 텍스트 생성
			return d.tdesc;
		},

		ct_title : function(d){ //타겟 설명 텍스트 생성
			return d.title;
		},

		ct_phase : function(d){ //타겟 설명 텍스트 생성
			return d.phase;
		},

		imageToolTip : function(d){ //tooltip 이미지 생성
			molecule_img(d.mdl);
			console.log(d.mdl);
			var imageThumnail = "<img id='mol_img1_0' class='mol_img1' src='../../img/common/none.png' style='background-color:white; border:1px solid rgba(255, 91, 95, 0.7); border-radius: 0px 3px 3px 3px; position:absolute; margin-top:5px; margin-left:-5px; box-shadow: 5px 5px 5px 3px gray;'>";

			return imageThumnail;
		},

		pdb_imageToolTip : function(pmdl){ //단백질 이미지 툴팁 생성
			//pdb_img(pmdl);
			if(pmdl != "" || pmdl != null){
				var imageThumnail = "<img id='mol_img1_0' class='mol_img1' src='../../img/PDB_IMG/"+pmdl+".jpg' style='background-color:white; border:1px solid rgba(255, 91, 95, 0.7); width:220px; height:220px; border-radius: 0px 3px 3px 3px; position:absolute; margin-top:5px; margin-left:-5px; box-shadow: 5px 5px 5px 3px gray;'>";
			}else{
				$('#mol_img1_0').attr('src', "../../img/common/no_img.jpg");
			}

			return imageThumnail;
		}
	}

}

//노드와 툴팁을 연결
function arrow(d, i, arrow_line){

	//배열에 들어있는 화살표만 작동
	if($.inArray($(".arrow_line_"+i).attr('class'), arrow_pool) != -1){
		var self = this;
		var t = d3.zoomTransform(self.svg.node()); //node의 내부 transform 정보 = 화살표 거리와 각도 계산을 위하여

		arrow_distance(d, i, t)
	}//if
}

//노드와 툴팁간의 거리 계산
function arrow_distance(d, i, t){

	var drag_width = $("#draggable_"+i).width();
	var drag_height = $("#draggable_"+i).height();

	var drag_position_left = $("#draggable_"+i).position().left;
	var drag_position_top = $("#draggable_"+i).position().top;

	var drag_position_right = drag_position_left+drag_width;
	var drag_position_bottom = drag_position_top+drag_height;

	var scale_change = t.k-1;  //해당 노드의 스케일 값이 반영 될때 변하는 translate을 잡아주기 위한 변수.

	var originX;
	var originY;
	var positionX;
	var positionY;

	$("#arrow_fix_icon_"+i).css({
		"width":"10px",
		"height":"10px",
		"background-color":"black",
		"opacity":"0.7",
		"position":"absolute",
		"z-index":"3",
		"border-radius":"70px"
	})

	if($('.arrow_line_'+i).length > 0){
		originX = d.x*t.k+t.x+radius/2+1/t.k+radius/2-6;
		originY = d.y*t.k+t.y+radius/2+1/t.k+radius/2+270;

		if(d.y+300+t.y+(d.y * scale_change) >= drag_position_top+drag_height/2 && d.x+t.x+(d.x * scale_change) < drag_position_left+drag_width/2){
			positionX = drag_position_left+1/t.k;
			positionY = drag_position_bottom+1/t.k;
			$("#arrow_fix_icon_"+i).css({'top': drag_height-5, "left": "-5px"})

		}else if(d.y+300+t.y+(d.y * scale_change) > drag_position_top+drag_height/2 && d.x+t.x+(d.x * scale_change) > drag_position_left+drag_width/2){
			positionX = drag_position_right+1/t.k;
			positionY = drag_position_bottom+1/t.k;
			$("#arrow_fix_icon_"+i).css({'top': drag_height-5, "left": drag_width-5})

		}else if(d.x+t.x+(d.x * scale_change) <= drag_position_left+drag_width/2){
			positionX = drag_position_left+1/t.k;
			positionY = drag_position_top+1/t.k;
			$("#arrow_fix_icon_"+i).css({'top': "-5px", "left": "-5px"})

		}else if(d.x+t.x+(d.x * scale_change) > drag_position_left+drag_width/2){
			positionX = drag_position_right+1/t.k;
			positionY = drag_position_top+1/t.k;
			$("#arrow_fix_icon_"+i).css({'top': "-5px", "left": drag_width-5})

		}


		var length = Math.sqrt((positionX - originX)*(positionX - originX)
			+ (positionY - originY)*(positionY - originY))

		var angle = 180/3.1415 * Math.acos((positionY - originY) / length);

		if(positionX > originX){
			angle *= -1;
		}
		//화살표 노드 위치지정
		//cos x축 sin y축
		/* 	x1 = d.x+(Math.cos(angle)*radius);
            y1 = d.y+(Math.sin(angle)*radius); */

		$(".arrow_line_"+i).css({
			"top" : d.y*t.k+t.y + radius/2+272, //svg가 margin에 의하여 하단에 위치하기에 margin값만큼 더해줌(+325)
			"left" : d.x*t.k+t.x + radius/2-2
		})
		$(".arrow_line_"+i).css({
			'height': length,
			'-webkit-transform': 'rotate(' + angle + 'deg)',
			'-moz-transform': 'rotate(' + angle + 'deg)',
			'-o-transform': 'rotate(' + angle + 'deg)',
			'-ms-transform': 'rotate(' + angle + 'deg)',
			'transform': 'rotate(' + angle + 'deg)',
		})
	}
}


function removeTooltip() {
	$("#mol_img1_0").remove(); //화합물 그림 제거
	$("#marvinjs-iframe").remove(); //화합물 그림 감싸는 wrap 제거
	$("#target_description").remove(); //타겟 description 제거

	//d3.select(".molecule_label").remove();
}

//화합물 이미지 생성
function molecule_img(mdl) {

	var molecules = new Array();
	molecules.push(mdl);

	var marvin;

	$(document).ready(function handleDocumentReady (e) {

		$('body').append($('<iframe>', { id: "marvinjs-iframe", style: "display:none;", src: "../../_common/util/marvin_js/marvinpack.html"}));

		MarvinJSUtil.getPackage("#marvinjs-iframe").then(function (marvinNameSpace) {
			marvinNameSpace.onReady(function() {
				marvin = marvinNameSpace;
				exportImages();
			});
		},function (error) {
			alert("Cannot retrieve marvin instance from iframe:"+error);
		});
	});

	function exportImages() {

		$("#imageContainer").empty();

		$.each(molecules, function(index, value) {

			//var imgData = marvin.ImageExporter.molToDataUrl(value);	//absolute 표시 (Absolute 표기는 화합물 구조의 특성 중 chiral center를 갖는 경우 나타남)
			imgData = marvin.ImageExporter.molToDataUrl(value, "image/png",{ "chiralFlagVisible": false });	//absolute 표시안함

			if(imgData != null)
				$('#mol_img1_'+index).attr("src", imgData);
			else
				$('#mol_img1_'+index).attr("src", "../../img/common/no_img.jpg");

		});

	}

}


//단백질 이미지
function pdb_img(pmdl, i){
	var pdb_molecules = new Array();
	pdb_molecules.push(pmdl);

	$.each(pdb_molecules, function(index, value) {

		if(pmdl != '' || pdml != null){
			imgData = "../../img/PDB_IMG/"+value+".jpg";
			$('#mol_img1_'+index + i).attr("src", imgData);
		}else{
			$('#mol_img1_0').attr('src', "../../img/common/no_img.jpg");
		}

	});
}




//색상 함수
function colors_closer(){

	return {
		palette : function(group){
			if(group == 1){
				return "#FF0000";
			}else if(group == 2){
				return "#FFAAA8";
			}else if(group == 3){
				return "#CC723D";
			}else if(group == 4){
				return "#F2CB61";
			}else if(group == 5){
				return "#FF00FF";
			}else if(group == 6){
				return "#47C83E";
			}else if(group == 7){
				return "#6799FF";
			}else if(group == 8){
				return "#D1B2FF";
			}else if(group == 9){
				return "#7228FF";
			}
		},


		link_palette :function(group){

			if(group == 1){
				return "#2F6156";
			}else if(group == 2){
				return "#CE7CAF";
			}else if(group == 3) {
				return "#3d75bf";
			}else{
				return "#bfa0a6";
			}
		}
	}
}




/**********
 *
 * on click 기능 여기에 넣어둠
 * 클로저 안에서는 정상적인 동작이 이루어지지않음
 *
 * ***********/

//고정툴팁 클릭시 삭제.
$(document).on('click', '.boxline_tip', function(e){

	var splice_tooltip = $(this).attr('id');
	$('#'+splice_tooltip).remove();
	fixed_tooltip_array.splice(splice_tooltip);
	fixed_tooltip_unique.splice(splice_tooltip);
})


//NGL 3d VIEW 로 넘어가기 위한 함수
$(this).on('click', function(e){
	if($(e.target).is('.ngl_search')){ //class 명으로 ngl_search 태그인지 체크
		pdb_id = $(e.target).attr('id') //id값 가져오기
		pdb_nm = pdb_obj[pdb_id]

		ngl_search(pdb_nm) //단백질 이름 넘기기
	}
})


function ngl_search(pdb_nm){
	alert(pdb_nm);
	$('input[name=search_pdb]').attr("value", pdb_nm);
	$('form[name=ngl_form]').attr("action", USER_HTML_LOCATION + "?depth=service/ngl_view_screening");
	$('form[name=ngl_form]').submit();

}

/***************************************/