import Image from "next/image";

const leftNavLinks = [
  { title: "Как все работает?" },
  { title: "Классифицировать" },
  { title: "Контакты" },
];

// Доделать header

export default function Header() {
  return (
    <header className="items-center py-10  m-auto text-xl uppercase max-w-7xl">
      <div className="flex justify-evenly items-center  py-4 border-black border-t-2 border-l-2 border-r-2">
        <nav className="ml-4">
          <ul className="flex space-x-4">
            {leftNavLinks.map((link) => (
              <li key={link.title}>
                <a href="#" className="text-gray-900 hover:text-gray-600">
                  {link.title}
                </a>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </header>
  );
}
