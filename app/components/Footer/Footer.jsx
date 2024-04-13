"use client";
import { Typography } from "@material-tailwind/react";

export default function Footer() {
  return (
    <div className="flex max-w-7xl m-auto justify-between mt-40 mb-10">
      <div className="flex flex-col border-black border-t-2 border-b-2">
        <div className="h-4 border-black border-l-2 border-r-2"></div>
        <div className="flex flex-row gap-20 justify-between items-start">
          <div className="text-left px-10">
            <Typography className="text-purple-400 text-xl">
              Контакты
            </Typography>
            <Typography className="py-2 underline decoration-solid text-xl">
              autopatent@gmail.com
            </Typography>
            <Typography className="py-2 underline decoration-solid text-xl">
              @tgautopatent
            </Typography>
          </div>
          <div className="px-10">
            <Typography className="text-purple-400 text-xl">
              Документы
            </Typography>
            <Typography className="py-2 underline decoration-solid text-xl ">
              политика конфиденциальности
            </Typography>
            <Typography className="py-2 underline decoration-solid text-xl">
              согласие на обработку персональных данных
            </Typography>
            <Typography className="py-2 underline decoration-solid text-xl">
              публичная оферта
            </Typography>
          </div>
        </div>
        <div className="h-2 border-black border-l-2 border-r-2"></div>
      </div>
      <div className="flex flex-col items-start justify-center pl-10">
        <Typography className="items-start text-5xl">
          Doc Classificator
        </Typography>
      </div>
    </div>
  );
}
