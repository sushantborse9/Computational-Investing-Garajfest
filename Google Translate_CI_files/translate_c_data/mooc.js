window._BFD=window._BFD||{};_BFD.addEvent=function(e,d,f){if(e.addEventListener){e.addEventListener(d,f,false)}else{if(e.attachEvent){e.attachEvent("on"+d,function(){f.call(e)})}else{e["on"+d]=f}}};_BFD.removeEvent=function(e,d,f){if(e.removeEventListener){e.removeEventListener(d,f,false)}else{if(e.detachEvent){e.detachEvent("on"+d,function(){f.call(e)})}else{e["on"+d]=null}}};_BFD.createElement=function(g,f){var h=document.createElement(g);if(f){for(var e in f){if(f.hasOwnProperty(e)){if(e==="class"||e==="className"){h.className=f[e]}else{if(e==="style"){h.style.cssText=f[e]}else{h.setAttribute(e,f[e])}}}}}return h};_BFD.loadScript=function(d,c){setTimeout(function(){var a=_BFD.createElement("script",{src:d,type:"text/javascript"});if(a.readyState){_BFD.addEvent(a,"readystatechange",function(){if(a.readyState==="loaded"||a.readyState==="complete"){if(c){c()}_BFD.removeEvent(a,"readystatechange",arguments.callee)}})}else{_BFD.addEvent(a,"load",function(){if(c){c()}_BFD.removeEvent(a,"load",arguments.callee)})}document.getElementsByTagName("head")[0].appendChild(a)},0)};_BFD.getByAttribute=function(l,k,j){var i=[],j=(j)?j:document,n=j.getElementsByTagName("*"),o=new RegExp("\\b"+k+"\\b","i");for(var p=0;p<n.length;p++){var m=n[p];if(l==="className"||l==="class"){if(o.test(m.className)){i.push(m)}}else{if(m.getAttribute(l)===k){i.push(m)}}}return i};_BFD.getByClass=function(c,d){return _BFD.getByAttribute("className",c,d)};_BFD.getById=function(b){if(typeof b==="string"&&!!b){return document.getElementById(b)}};_BFD.loadCss=function(d){var c=_BFD.createElement("link",{href:d,rel:"stylesheet",type:"text/css"});document.getElementsByTagName("head")[0].appendChild(c)};_BFD.insertAfter=function(g,h){var e=h.parentNode;if(e.lastChild==h){e.appendChild(g)}else{var f=h.nextElementSibling||h.nextSibling;e.insertBefore(g,f)}};_BFD.Banner=function(a,c){this.callback=c;this.positionstr=a.pos_dom;this.bid=a.bid;if(a.json_args){this.json_str=b(a.json_args)}else{this.json_str="{}"}this.div_id="bfd_"+a.bid;this.div_class_name="bfd_border";function b(e){var f=[];for(var d in e){f.push('"'+d+'":"'+e[d]+'"')}return"{"+f.join(",")+"}"}};_BFD.handleResults=function(h,d){if(d&&d[2]&&d[2].length>0){var g=d[2];for(var c=0;c<g.length;c++){var f=h[c];var e=g[c][3];var b=g[c][2];var a=f.bid;if(e&&e.length>0){f.callback(e,b,a)}}}};_BFD.parseBanners=function(b,f,g){var e=[],a=[];for(var c=0,d;d=f[c++];){e.push(d.bid);if(d.json_str&&d.json_str.length>0&&d.json_str!="{}"){a.push("rec_"+d.bid+"$"+d.json_str)}else{a.push("rec_"+d.bid)}}if(f.length){b.bidlst=e.join("|");b.req=a.join("|");g.send(b,function(h){_BFD.handleResults(f,h)})}};_BFD.loadScript(("https:"==document.location.protocol?"https://ssl-static":"http://static")+".baifendian.com/api/2.0/bcore.min.js",function(){var d=new $Core(function(){});var b=$Core.tools.Tools;d.options.cid=_BFD.client_id;d.options.uid=_BFD.BFD_INFO.user_id;d.options.d_s="pc";if(typeof(d.options.uid)=="undefined"||d.options.uid==""||d.options.uid=="0"||d.options.uid==null){d.options.uid=d.options.sid}var a=new $Core.inputs.JObject();a.iid="$id";a.name="$title";a.url="$url";a.img="$picture";BCore.recommends.Recommend.prototype.fmt=a.toString();_BFD.bfd_show=function(g,f,e){var h=_BFD.show_recommended();_BFD.show_template(g,h,f,e)};_BFD.show_recommended=function(){};_BFD.show_content=function(f,e){};_BFD.show_template=function(e,h,g,f){};_BFD.banners={hp:[],ls:[],dt:[],"default":[]};var c=(function(){function e(){if(!_BFD.BFD_INFO){_BFD.BFD_INFO={}}else{var f=this[_BFD.BFD_INFO.page_type];if(f&&typeof f==="function"){f.call(this,d)}else{if(location.href=="http://mooc.guokr.com/"){this.homepage(d)}else{if(location.href.indexOf("post")!=-1&&_BFD.getByClass("content-th",document)[0]){this.detail(d)}else{if(location.href.indexOf("course")!=-1&&_BFD.getByClass("course-title ch",document)[0]){this.detail(d)}else{if(location.href.indexOf("college")!=-1&&_BFD.getByClass("school-info-data",document)[0]){this.detail(d)}else{this.dft(d)}}}}}}}e.prototype={homepage:function(g){g.options.p_t="hp";var f=new $Core.inputs.PageView();f.p_p="";g.send(f)},detail:function(y){y.options.p_t="dt";var I=new $Core.inputs.PageView();I.p_p="";y.send(I);var j=location.href;if(location.href.indexOf("course")!=-1){var p=_BFD.getByClass("course-title",document)[0].getElementsByTagName("a")[0].title;var G=location.href.split("course/")[1].split("/")[0];var l=(function(){if(_BFD.getByClass("course-start",document)[0]){var i=_BFD.getByClass("course-start",document)[0].innerHTML.split("：")[1];return i}})();function h(V){var i=new Date();i.setFullYear(V.substring(0,4));i.setMonth(V.substring(5,7)-1);i.setDate(V.substring(8,10));return Date.parse(i)/1000}var g=(function(){if(_BFD.getByClass("tabs-num",document)[0]){var i=_BFD.getByClass("tabs-num",document)[0].innerHTML;return i}})();var n=(function(){if(_BFD.getByClass("vjs-tech",document)[0]){var i=_BFD.getByClass("vjs-tech",document)[0].poster;return i}else{if(_BFD.getByClass("course-img",document)[0]){var i=_BFD.getByClass("course-img",document)[0].getElementsByTagName("img")[0].src;return i}}})();var N=(function(){if(_BFD.getByClass("course-title ch",document)[0]){var i=_BFD.getByClass("course-title ch",document)[0].getElementsByTagName("a")[0].innerHTML;return i}})();var m=[];if(_BFD.getByClass("active",document)[0]){var z=_BFD.getByClass("active",document)[0];if(z.getElementsByTagName("a")[0]){var w=z.getElementsByTagName("a")[0];var H=w.href;var B=w.innerHTML;var C=[];C.push(B);C.push(H);m.push(C)}}if(_BFD.getByClass("course-info",document)[0]){var z=_BFD.getByClass("course-info",document)[0];if(z.getElementsByTagName("a")[1]){var w=z.getElementsByTagName("a")[1];var H=w.href;var B=w.innerHTML.replace(/\s/g,"");var C=[];C.push(B);C.push(H);m.push(C)}}}if(location.href.indexOf("post")!=-1){var D=_BFD.getById("contentTitle",document).innerHTML;var G=location.href.split("post/")[1].split("/")[0];function K(V){var i=new Date();i.setFullYear(V.substring(0,4));i.setMonth(V.substring(5,7)-1);i.setDate(V.substring(8,10));i.setHours(V.substring(11,13));i.setMinutes(V.substring(14,16));i.setSeconds(V.substring(17,19));return Date.parse(i)/1000}function k(X){var V=new Date();V.setDate(V.getDate()+X);var Y=V.getFullYear();var i=V.getMonth()+1;if(i<10){i="0"+i}var W=V.getDate();return Y+"-"+i+"-"+W+" "}var l="";if(_BFD.getByClass("post-time",document)[0]){var x=_BFD.getByClass("post-time",document)[0];if(_BFD.getByClass("post-time",document)[0]){var Q=_BFD.getByClass("post-time",document)[0].innerHTML;var A=Q;Q=Q.replace("-","/");Q=Q.replace("-","/");if(Q.indexOf("今天")!=-1){as=Q.replace("今天",k(0));l=K(as)}else{if(Q.indexOf("昨天")!=-1){as=Q.replace("昨天",k(-1));l=K(as)}else{if(Q.indexOf("前天")!=-1){as=Q.replace("前天",k(-2));l=K(as)}else{if(Q.indexOf("小时")!=-1){var P=new Date();var u="-";var t=":";var f=P.getMonth()+1;var q=P.getDate();if(f>=1&&f<=9){f="0"+f}if(q>=0&&q<=9){q="0"+q}var o=P.getFullYear()+u+f+u+q+" "+P.getHours()+t+P.getMinutes();l=K(o)}else{if(Q.indexOf("分钟")!=-1){var P=new Date();var u="-";var t=":";var f=P.getMonth()+1;var q=P.getDate();if(f>=1&&f<=9){f="0"+f}if(q>=0&&q<=9){q="0"+q}var o=P.getFullYear()+u+f+u+q+" "+P.getHours()+t+P.getMinutes();l=K(o)}else{l=K(Q)}}}}}}}var J=(function(){if(_BFD.getByClass("post-author",document)[0]){var i=_BFD.getByClass("post-author",document)[0].getElementsByTagName("a")[0].title;return i}})();var g=(function(){if(_BFD.getByClass("cmts-title-num",document)[0]){var i=_BFD.getByClass("cmts-title-num",document)[0].innerHTML.split("（")[1].split("条")[0];return i}})()}if(location.href.indexOf("college")!=-1){var p=_BFD.getByClass("info-data-name en",document)[0].innerHTML;var G=location.href.split("college/")[1].split("/")[0];var n=(function(){if(_BFD.getByClass("school-info-logo",document)[0]){var i=_BFD.getByClass("school-info-logo",document)[0].src;return i}})();var N=(function(){if(_BFD.getByClass("info-data-name ch",document)[0]){var i=_BFD.getByClass("info-data-name ch",document)[0].innerHTML;return i}})();var r=(function(){if(_BFD.getByClass("info-data-location",document)[0]){var i=_BFD.getByClass("info-data-location",document)[0].innerHTML.replace(/\s/g,"").split("：")[1];return i}})();var m=[];if(_BFD.getByClass("course-info",document)[0]){var z=_BFD.getByClass("course-info",document)[0];if(z.getElementsByTagName("a")[1]){var w=z.getElementsByTagName("a")[1];var H=w.href;var B=w.innerHTML.replace(/\s/g,"");var C=[];C.push(B);C.push(H);m.push(C)}}}var T=(function(){return true})();y.send(new BCore.inputs.Visit(G));var S=[];if(m&&m instanceof Array){for(var O=0;O<m.length;O++){S.push(m[O][0])}}if(!T){y.send(new $Core.inputs.RmItem(G))}else{if(location.href.indexOf("course")!=-1){var R=new $Core.inputs.AddItem(G);R.title=N;R.url=j;R.cat=S;if(l.indexOf("时间自主")!=-1){R.ptime=" "}else{R.ptime=h(l)}var U=document.getElementsByTagName("meta");if(U){var s=document.getElementsByTagName("meta")[1].content}if(s){var E=s.replace(/\，/g,",");R.keywords=E}R.img=n;R.ccnt=g;var M=new $Core.inputs.JObject();M.Etitle=p;R.attr=M.toString();y.send(R)}else{if(location.href.indexOf("post")!=-1){if(location.href.indexOf("page=3")!=-1||location.href.indexOf("page=2")!=-1||location.href.indexOf("page=2")!=-1){var R=new $Core.inputs.AddItem(G);R.title=D;R.ptime=l;var U=document.getElementsByTagName("meta");if(U){var s=document.getElementsByTagName("meta")[1].content}if(s){var E=s.replace(/\，/g,",");R.keywords=E}R.author=J;R.ccnt=g}else{var R=new $Core.inputs.AddItem(G);R.title=D;R.ptime=l;var U=document.getElementsByTagName("meta");if(U){var s=document.getElementsByTagName("meta")[1].content}if(s){var E=s.replace(/\，/g,",");R.keywords=E}R.author=J;R.ccnt=g;y.send(R)}}else{if(location.href.indexOf("college")!=-1){var R=new $Core.inputs.AddItem(G);R.title=N;var M=new $Core.inputs.JObject();M.Etitle=p;R.loc=r;R.img=n;var U=document.getElementsByTagName("meta");if(U){var s=document.getElementsByTagName("meta")[1].content}if(s){var E=s.replace(/\，/g,",");R.keywords=E}R.attr=M.toString();y.send(R)}}}}if(S.length>0){var F=S[S.length-1];y.send(new $Core.inputs.VisitCat(S.join("$")));var L=new $Core.inputs.AddCat(F);if(m.length>0){L.url=m[m.length-1][1];var v=m.concat();v.pop();L.ptree=new $Core.inputs.JObject().toString(v);y.send(L)}}},dft:function(g){g.options.p_t="dft";var f=new $Core.inputs.PageView();f.p_p="";g.send(f)}};return e})();new c()});