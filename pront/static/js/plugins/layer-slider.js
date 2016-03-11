var LayerSlider = function () {
    return {
        initLayerSlider: function () {
		    $(document).ready(function(){
		        jQuery("#layerslider").layerSlider({
			        skin: 'fullwidth',
			        responsive : true,
			        responsiveUnder : 960,
			        layersContainer : 960,
			        skinsPath: 'static/plugins/layer-slider/layerslider/skins/'
			    });
		    });     
        }
    };
}();        