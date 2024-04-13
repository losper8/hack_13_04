"use client";
import { Button, Chip, Input, Typography } from "@material-tailwind/react";

import Image from "next/image";

export default function Body() {
  return (
    <div className="flex items-center  max-w-7xl bg-[url('/backgrounds/main.svg')]  bg-no-repeat m-auto h-[701px] ">
      <div className={`max-w-6xl mx-auto flex-col items-center`}>
        <div className="flex items-center justify-end gap-2">
          {/* <Typography className="text-2xl font-light">генерируем</Typography> */}
          <Chip
            className="text-sm font-medium rounded-full"
            value="генерируем время"
            variant="gradient"
            color="purple"
          />
        </div>
        <Typography
          variant="h1"
          className="flex justify-center items-center m-auto p-1 font-body  text-9xl"
        >
          Doc Classificator
        </Typography>

        <Button
          color="purple"
          variant="gradient"
          className=" rounded-full text-2xl font-medium items-center w-[48rem]  m-auto p-auto block"
        >
          Начать работу
        </Button>
      </div>
    </div>
  );
}
