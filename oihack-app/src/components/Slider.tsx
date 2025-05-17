// import Image from "next/image";
import SliderItem from '@/components/templates/SliderItem';

interface SliderProps {
    items: {
        id: string,
        image: string,
        title: string
    }[]
}

export default function Slider( { items }: SliderProps) {
    return (
        <div className="wrapper mt-[28px]">
            <div className="slider flex gap-[12px] overflow-x-auto scrollbar-hide snap-x snap-mandatory">
                {items.map((item) => (
                    <SliderItem key={item.id} title={item.title} image={item.image} />
                ))}
            </div>
        </div>
    );
}