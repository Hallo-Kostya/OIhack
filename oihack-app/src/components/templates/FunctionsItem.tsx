import Image from "next/image";

interface FunctionsItemProps {
    icon: string;
    image: string;
    title: string;
}

export default function FunctionsItem( {icon, image, title}: FunctionsItemProps) {
    return (
        <div 
        style={{borderColor: 'rgba(75, 75, 75, 0.6)'}}
        className="function-item relative w-[162px] h-[160px] border-[1px] rounded-[12px] overflow-hidden">
            {/* Фоновое изображение */}
            <Image
                src={image}
                alt={title}
                width={100}
                height={100}
                className="absolute bottom-0 right-0"
            />

            {/* Серый круг для иконки */}
            <div 
            style={{borderColor: 'rgba(75, 75, 75, 0.6)'}}
            className="icon-circle absolute border-[0.6px] bg-opacity-[0.1] top-[8px] left-[8px] w-[36px] h-[36px] bg-[#504F4F] rounded-full flex items-center justify-center">
                <Image
                src={icon}
                alt={title}
                width={24}
                height={24}
                className="w-6 h-6"
                />
            </div>

            {/* Заголовок */}
            <p className="text-[16px] text-white font-[300] absolute bottom-1 right-2">
                {title}
            </p>
        </div>
    );
}