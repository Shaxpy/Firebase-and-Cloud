const admin = require('./node_modules/firebase-admin');
const serviceAccount = require("./serviceAccountKey.json");
const data = require("./data.json");
const collectionKey = "Stuff"; // name of the collection
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "DBMS URL (@users and permissions)" //  Can't reveal that here!:)
});
const firestore = admin.firestore();
const settings = {timestampsInSnapshots: true};
firestore.settings(settings);
if (data && (typeof data === "object")) {
Object.keys(data).forEach(docKey => {
 firestore.collection(collectionKey).doc(docKey).set(data[docKey]).then((res) => {
    console.log("Document " + docKey + " successfully written!");
}).catch((error) => {
   console.error("Error writing document: ", error);
});
});
}
