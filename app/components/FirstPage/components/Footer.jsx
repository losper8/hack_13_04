import { Typography } from "@material-tailwind/react";

export default function Footer() {
  return (
    <div className="max-w-7xl border-b-2 border-r-2 border-l-2 m-auto border-black mt-10 pb-2">
      <Typography className="flex justify-center text-center text-xl">
        Определяем тип документа <br /> с помощью алгоритмов <br />
        исскусственного интеллекта
      </Typography>
    </div>
  );
}
