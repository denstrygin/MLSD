import { Fragment } from "react";

function SemanticComponent({image, image_masks, list_of_symbols, nameFile}: {image: any, image_masks: any[], list_of_symbols: {semantic: string, symbol: string, color: string[]}[], nameFile: string}) {
    function getImage(image: any) {
        const IMAGE_SIZE: number = 256
        const canvas = document.createElement('canvas');
        canvas.width = IMAGE_SIZE;
        canvas.height = IMAGE_SIZE;
        const ctx: any = canvas.getContext('2d');
        const imageData = ctx.createImageData(IMAGE_SIZE, IMAGE_SIZE);
        const flatImage = image.flat();
        for (let i = 0, j = 0; i < flatImage.length; i++, j += 4) {
            imageData.data[j] = flatImage[i][0];
            imageData.data[j + 1] = flatImage[i][1];
            imageData.data[j + 2] = flatImage[i][2];
            imageData.data[j + 3] = 255;
        }
        ctx.putImageData(imageData, 0, 0);
        return canvas.toDataURL();
    }
    const imageUrl = getImage(image)
    const maskUrl = image_masks.map(item => getImage(item))

    return (
        <div className="w-full p-4 lg:p-12 bg-white rounded shadow-[0_2px_8px_rgba(0,0,0,0.25)]">
            <span className="font-bold font-sans text-4xl">{nameFile}</span>
            <div className="w-full mt-8 grid grid-cols-1 xs:grid-cols-3 gap-2.5 ">
                {maskUrl.map((item, index) =>
                    <Fragment key={index}>
                        <img src={ imageUrl } className="shadow-lg hidden xs:block" alt="canvas" />
                        <div className="relative">
                            <img src={ imageUrl } className="shadow-lg w-full lg:w-auto" alt="canvas" />
                            <img src={ item } className="shadow-lg w-full lg:w-auto absolute top-0 left-0 opacity-70" alt="mask" />
                        </div>
                        <img src={ item } className="shadow-lg hidden xs:block" alt="mask" />   
                    </Fragment>
                )}
            </div>
            <div className="flex flex-col">
                {list_of_symbols.map((item, index) =>
                    <Fragment key={index}>
                        <div className="flex items-baseline">
                            <span className="font-bold">{item.symbol}</span>
                            <div className="w-[10px] h-[10px] ml-1" style={{backgroundColor: `rgb(${item.color[0]}, ${item.color[1]}, ${item.color[2]})`}}></div>
                        </div>
                        <ul className="list-disc pl-6">
                            {item.semantic.split('; ').map((item, index) => <li key={index} className="text-start">{item}</li>)}
                        </ul>
                    </Fragment>
                )}
            </div>
        </div>
    );
}

export default SemanticComponent;