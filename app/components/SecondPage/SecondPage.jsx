"use client";
import { Typography } from "@material-tailwind/react";
import Dropzone from "./components/Dropzone";

export default function SecondPage() {
  return (
    <div className="flex flex-col max-w-7xl m-auto mt-10 ">
      <Typography className="text-6xl border-t-2 border-l-2 border-r-2 border-black p-auto p-10">
        Начать классификацию сейчас
      </Typography>
      <div className="flex justify-evenly items-center">
        <Dropzone />
        {/* <Typography>Заглушка</Typography> */}
      </div>
    </div>
  );
}
