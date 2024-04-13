import Image from "next/image";

const leftNavLinks = [
  { title: "Как все работает?", target: "howItWorks" },
  { title: "Классификатор", target: "classify" },
  { title: "Контакты", target: "footer" },
];

// Доделать header

export default function Header() {
  const scrollToSection = (targetId) => {
    const targetElement = document.getElementById(targetId);
    if (targetElement) {
      window.scrollTo({
        top: targetElement.offsetTop,
        behavior: "smooth",
      });
    }
  };

  return (
    <header className="items-center py-10  m-auto text-xl uppercase max-w-7xl">
      <div className="flex justify-evenly items-center  py-4 border-black border-t-2 border-l-2 border-r-2">
        <nav className="ml-4">
          <ul className="flex space-x-4">
            {leftNavLinks.map((link) => (
              <li key={link.title}>
                <button
                  onClick={() => scrollToSection(link.target)}
                  className="text-gray-900 hover:text-gray-600"
                >
                  {link.title}
                </button>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </header>
  );
}
