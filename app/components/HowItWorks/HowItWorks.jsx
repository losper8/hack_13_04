"use client";
import { Typography } from "@material-tailwind/react";
import Image from "next/image";

export default function HowItWorks({ id }) {
  return (
    <div
      id={id}
      className="flex flex-col max-w-7xl border-black m-auto mt-20 border-t-2 border-r-2"
    >
      <div className="h-[55px] border-l-2 border-black"></div>
      <Typography className="text-8xl p-10">Как это работает?</Typography>
      <div className="flex flex-row m-auto mt-10 justify-between py-10">
        <video
          className="rounded-lg w-[670px] h-auto align-middle py-10"
          controls
        >
          <source
            src="https://docs.material-tailwind.com/demo.mp4"
            type="video/mp4"
          />
          Your browser does not support the video tag.
        </video>
        <div className="flex flex-col ml-10  justify-between ">
          <Typography className="text-lg font-light">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit,
            quibusdam maxime provident ratione dolorum architecto repellat,
            neque culpa quidem nam voluptatibus eligendi libero itaque harum
            magni fugiat ut consectetur cumque.
          </Typography>
          <Typography className="text-lg">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit
          </Typography>
          <Typography className="text-lg">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit
          </Typography>
          <ol className="ml-4 text-lg">
            <li>
              1.{" "}
              <a className="text-purple-400 hover:text-purple-700 hover:cursor-pointer">
                Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit{" "}
              </a>
              в "поисковую строку" на сайте
            </li>
            <li>
              2. Нажать на кнопку{" "}
              <a className="text-purple-400 hover:text-purple-700 hover:cursor-pointer">
                "Поиск"
              </a>
            </li>
            <li>
              3.{" "}
              <a className="text-purple-400 hover:text-purple-700 hover:cursor-pointer">
                Выбрать кластер
              </a>{" "}
              из предложенных, к которому относится патентное исследование
            </li>
            <li>
              4. Нажать кнопку{" "}
              <a className="text-purple-400 hover:text-purple-700 hover:cursor-pointer">
                "Сгенерировать"
              </a>
            </li>
          </ol>
          <Typography className="text-lg">
            Более подробный план действий представлен на видео
          </Typography>
        </div>
      </div>
    </div>
  );
}
