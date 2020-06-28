/* global Cesium */

const viewer = new Cesium.Viewer('cesiumContainer', {
    terrianProvider: Cesium.createWorldTerrain(),
});
const scene = viewer.scene;
const globe = scene.globe;

scene.screenSpaceCameraController.enableCollisionDetection = false;
globe.translucency.frontFaceAlphaByDistance = new Cesium.NearFarScalar(
    400.0,
    0.0,
    2000.0,
    0.9,
);
globe.translucency.enabled = true;

const tokyo = {
    lat: 35.60,
    lng: 139.8033,
};

const ds = Cesium.CzmlDataSource.load('/test.czml');
viewer.dataSources.add(ds);

viewer.camera.setView({
    destination: Cesium.Cartesian3.fromDegrees(
        tokyo.lng, tokyo.lat, 10000,
    ),
    orientation: {
        heading: Cesium.Math.toRadians(0),
        pitch: Cesium.Math.toRadians(-45),
    },
});
