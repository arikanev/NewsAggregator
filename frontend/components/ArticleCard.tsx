import Image from 'next/image';

export default function ArticleCard({ title, date, category, content }: any) {
  return (
    <div className="p-4 rounded-md border border-slate-200 flex-grow cursor-pointer hover:border-slate-300 hover:shadow-md hover:scale-[101%] hover:bg-slate-100/20 transition-all">
      <div className="bg-slate-100 rounded-md aspect-video w-full relative overflow-hidden grayscale">
        <Image
          className="aspect-video"
          fill={true}
          src={`/${category}.png`}
          alt="thumbnail"
        />
      </div>
      <h3 className="mt-2 scroll-m-20 text-xl font-semibold tracking-tight">{title}</h3>
      <p className="text-sm text-slate-500 dark:text-slate-400">{date}</p>
    </div>
  );
}

