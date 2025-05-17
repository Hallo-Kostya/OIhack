import Image from "next/image";

interface SliderItemProps {
    image: string;
    title: string;
}

export default function SliderItem( {image, title}: SliderItemProps) {
    return (
        <div className="wrapper relative w-[96px] h-[96px] shrink-0 rounded-md overflow-hidden">
            <Image
                src={image}
                alt={title}
                width={96}
                height={96}
                className="w-full h-full object-cover"
            />
            <p className="eventname absolute bottom-1 left-[6.55px] text-[7.64px] font-[700] text-[#FFFFFF]">
                {title}
            </p>
        </div>
    );
}