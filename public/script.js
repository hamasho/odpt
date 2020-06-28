/* global Cesium */

const viewer = new Cesium.Viewer('cesiumContainer');

const tokyo = {
    lat: 35.645775,
    lng: 139.81033,
};

const ds = Cesium.CzmlDataSource.load('/test.czml');
viewer.dataSources.add(ds);

viewer.camera.flyTo({
    destination: Cesium.Cartesian3.fromDegrees(
        tokyo.lng, tokyo.lat, 100000,
    ),
});
