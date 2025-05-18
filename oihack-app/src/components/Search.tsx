import Image from "next/image";

export default function Search() {
    return (
        <div className="wrapper mt-[16px] flex items-center relative bg-[#393939] rounded-[8px] py-[8px] px-[12px]">
            <Image 
                src={"/common/components/search.svg"}
                width={24}
                height={24}
                alt={"Поиск"}
            >
            </Image>
            <a href='/chat'>
                <input
                    type="text"
                    placeholder={"Задайте свой вопрос"}
                    className="w-full h-full bg-transparent outline-none pl-[12px] text-[#828282]"
                />
            </a>
        </div>
    );
}