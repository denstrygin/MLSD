import DropBoxModel from './DropBoxModel';

interface ModelComponent {
    header: string
    imgUrl: string
    altImg: string
  }
  
const listOfModels: ModelComponent[] = [
  {
    header: 'Натюрморты застолья',
    imgUrl: './img/table3.jpg',
    altImg: 'натюрморт застолья',
  },
  {
    header: 'Цветочные натюрморты',
    imgUrl: './img/flower3.jpg',
    altImg: 'цветочный натюрморт',
  },
  {
    header: 'Ученые натюрморты',
    imgUrl: './img/skeleton3.jpg',
    altImg: 'суета сует',
  },
]

function SpecialModel() {
    return (
        <div className='w-[80%] flex flex-wrap justify-center gap-8'>
            {listOfModels.map((item, index) => <DropBoxModel 
                key={index} 
                idKey={index} 
                header={item.header} 
                imgUrl={item.imgUrl} 
                altImg={item.altImg} 
            />)}
        </div>
    );
}

export default SpecialModel;