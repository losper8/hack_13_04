import Image from "next/image";

import FirstPage from "./components/FirstPage/FirstPage";
import Footer from "./components/Footer/Footer";
import SecondPage from "./components/SecondPage/SecondPage";
import HowItWorks from "./components/HowItWorks/HowItWorks";

export default function Home() {
  return (
    <>
      <FirstPage />
      <HowItWorks />s
      <SecondPage />
      <Footer />
    </>
  );
}
