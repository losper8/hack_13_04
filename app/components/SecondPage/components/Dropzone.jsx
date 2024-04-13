"use client";
import { useState } from "react";
import { useDropzone } from "react-dropzone";
import { ArrowUpTrayIcon } from "@heroicons/react/24/solid";
import { Button, Alert, Typography } from "@material-tailwind/react";

export default function Dropzone(props) {
  const [files, setFiles] = useState([]);
  const [error, setError] = useState("");

  const { getRootProps, getInputProps } = useDropzone({
    accept: {
      "text/txt": [".txt"],
    },
    onDrop: (acceptedFiles) => {
      setFiles([...files, ...acceptedFiles]);
    },
    onDropRejected: (rejectedFiles) => {
      const rejectedFileNames = rejectedFiles.map((file) => file.name);
      setError(`Ошибка: Допустимы только файлы с расширением .txt.`);
      setTimeout(() => {
        setError("");
      }, 3000);
    },
  });

  const removeFile = (fileToRemove) => {
    const updatedFiles = files.filter((file) => file !== fileToRemove);
    setFiles(updatedFiles);
  };

  const fileList = files.map((file, index) => (
    <li key={index}>
      {file.path}
      <Button
        variant="gradient"
        color="red"
        size="sm"
        onClick={() => removeFile(file)}
        className="ml-2"
      >
        Удалить
      </Button>
    </li>
  ));

  return (
    <section className="container m-auto mt-10 max-w-7xl">
      <div
        {...getRootProps({
          className:
            "dropzone border-dashed border-black rounded-lg border-2 inline-block p-10 active:border-blue-800  hover:cursor-pointer",
        })}
      >
        <input {...getInputProps()} />
        <div className="m-auto p-auto">
          <ArrowUpTrayIcon className="h-10 w-10 m-auto" />
          <p>Перетащите сюда файлы</p>
          <p className="m-auto text-center">или</p>
          <Button
            variant="gradient"
            color="green"
            className="m-auto p-auto mt-2 block"
          >
            Выберите файлы
          </Button>
        </div>
      </div>
      <div className={error ? "animate-fadeOut" : ""}>
        {error && (
          <div className="fixed bottom-0 left-0 right-0 bg-red-500 text-white p-4 text-center">
            {error}
          </div>
        )}
      </div>
      <aside className="mt-5">
        <Typography variant="h4">Загруженные файлы:</Typography>
        <ul>{fileList}</ul>
      </aside>
      <Button variant="gradient" color="green" className="mt-5">
        Начать классификацию
      </Button>
    </section>
  );
}
