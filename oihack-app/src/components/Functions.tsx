import FunctionsItem from "@/components/templates/FunctionsItem";

interface FunctionsProps {
    functions: {
        id: string;
        icon: string;
        image: string;
        title: string;
    }[]
}

export default function Functions( { functions }: FunctionsProps) {
    return (
        <div className="wrapper mt-[44px]">
            <div className="grid grid-cols-2 gap-x-[19px] gap-y-[21px]">
                {functions.map((func) => (
                <FunctionsItem
                    key={func.id}
                    icon={func.icon}
                    image={func.image}
                    title={func.title}
                />
                ))}
            </div>
        </div>
    );
}