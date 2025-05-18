import Image from "next/image";
import Header from "@/components/Header";
import Search from "@/components/Search";
import Slider from "@/components/Slider";
import Functions from "@/components/Functions";
import Link from "next/link";

// Templates
const items = [
  {
    id: '1',
    image: '/common/components/default__event.png',
    title: 'День программиста',
  },
  {
    id: '2',
    image: '/common/components/default__event.png',
    title: 'День программиста',
  },
  {
    id: '3',
    image: '/common/components/default__event.png',
    title: 'День программиста',
  },
  {
    id: '4',
    image: '/common/components/default__event.png',
    title: 'День программиста',
  },
  {
    id: '5',
    image: '/common/components/default__event.png',
    title: 'День программиста',
  },
];

const functions = [
  {
    id: '1',
    icon: '/common/components/users.svg',
    image: '/common/functions/users.svg',
    title: 'Сотрудники',
  },
  {
    id: '2',
    icon: '/common/components/calendar.svg',
    image: '/common/functions/calendar.svg',
    title: 'Календарь',
  },
  {
    id: '3',
    icon: '/common/components/info.svg',
    image: '/common/functions/info.svg',
    title: 'О компании',
  },
  {
    id: '4',
    icon: '/common/components/events.svg',
    image: '/common/functions/events.svg',
    title: 'События',
  },
];

export default function Home() {
  return (
    <div className="">
      <Image
        src="/common/background_main.png"
        alt="Background"
        layout="responsive"
        width={375}
        height={812}
        objectFit="cover"
        quality={100}
        className="absolute inset-0 z-[-1] w-full h-full"
      />
      <main className="w-[343px] mx-auto">
        <Header user_name={"Константин"} />
        <Search />
        <Slider items={items} />
        <Functions functions={functions} />
      </main>
      <footer className="h-[95px] mt-20  bg-black/10">
          <div className="flex justify-center align-center gap-2 pt-5">
            <Link href={"https://www.interesnee.ru/"}>
              <Image 
                src={"/common/logo.png"} 
                alt={"Очень интересно"}
                width={24} 
                height={24}>
              </Image>
            </Link>
            <h1>Очень интересно</h1>
          </div>
          <h2 className="flex justify-center text-[14px] font-[300] mt-2 opacity-[0.8]">Россия, г. Екатеринбург</h2>
      </footer>
    </div>
  );
}
