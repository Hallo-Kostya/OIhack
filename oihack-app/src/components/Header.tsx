import Image from "next/image";

interface HeaderProps {
    user_name: string;
}

export default function Header({ user_name }: HeaderProps) {
    return (
        <div className="wrapper mt-[44px]">
            <div className="container flex justify-between">
                <div className="notifications w-[44px] h-[44px] rounded-full bg-[#414141] flex items-center justify-center">
                    <Image 
                        className="noti"
                        src={"/common/components/noti_false.svg"}
                        width={24}
                        height={24} 
                        alt={"Notifications"}
                    >
                    </Image>
                </div>
                <div className="profile flex gap-[8px]">
                    <p className="username text-[14px] font-[500] text-[#FFFFFF] my-auto">
                        {user_name}
                    </p>
                    <Image 
                        className="useravatar" 
                        src={"/common/components/default__avatar.svg"}
                        width={36}
                        height={36}
                        alt={"Avatar"}
                    >
                    </Image>
                </div>
            </div>
        </div>
    );
}