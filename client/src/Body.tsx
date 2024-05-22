import SpecialModel from './SpecialModel';
import SymbolWindow from './SymbolWindow';

function Body() {
    return (
        <div className='w-full flex justify-center font-serif p-4'>
            <SpecialModel />
            <SymbolWindow />
        </div>
    );
}

export default Body;