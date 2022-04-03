// function dark_mode() {
//   document.getElementsByTagName("body")[0].style =
//     "background-color: #212121;color: white;";
// }

// function light_mode() {
//   document.getElementsByTagName("body")[0].style =
//     "background-color: white;color: black !important;";
// }

/**
 * Preloader
 */
let preloader = select("#preloader");
if (preloader) {
  window.addEventListener("load", () => {
    preloader.remove();
  });
}

// Import the functions you need from the SDKs you need
        import { initializeApp } from "firebase/app";
        import { getAnalytics } from "firebase/analytics";
        // TODO: Add SDKs for Firebase products that you want to use
        // https://firebase.google.com/docs/web/setup#available-libraries

        // Your web app's Firebase configuration
        // For Firebase JS SDK v7.20.0 and later, measurementId is optional
        const firebaseConfig = {
        apiKey: "AIzaSyCXo9yReItwtL1OBEfXazVzX_tmUzJAbdk",
        authDomain: "cj-s-market.firebaseapp.com",
        projectId: "cj-s-market",
        storageBucket: "cj-s-market.appspot.com",
        messagingSenderId: "894102784909",
        appId: "1:894102784909:web:8394518848893cedeccbc4",
        measurementId: "G-N7RPP4FFYH"
        };

        // Initialize Firebase
        const app = initializeApp(firebaseConfig);
        const analytics = getAnalytics(app);

