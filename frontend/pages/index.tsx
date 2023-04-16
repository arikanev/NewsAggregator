import Image from 'next/image';
import Link from 'next/link';

import Head from 'next/head';
import { format } from 'date-fns';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import ArticleCard from '@/components/ArticleCard';
import { Button } from '@/components/ui/button';

import { useState } from 'react';

export default function Home() {
  const categories = ['Business', 'Tech', 'Politics', 'Sports', 'Entertainment'];
  const [url, setUrl] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<boolean>(false);

  const getSummary = async () => {
    console.log(url);
    setLoading(true);
    try {
      const res = await fetch(`https://9369-157-242-208-112.ngrok-free.app/summarize?url=${url}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      const json = await res.json();

      console.log(json);
    } catch {
      setLoading(false);
      setError(true);
    }
  };

  const Loading = () => {
    return (
      <div className="flex items-center">
        <div role="status">
          <svg
            aria-hidden="true"
            className="w-6 h-6 text-gray-200 animate-spin fill-blue-600"
            viewBox="0 0 100 101"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
              fill="currentColor"
            />
            <path
              d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
              fill="currentFill"
            />
          </svg>
          <span className="sr-only">Loading... this may take a minute</span>
        </div>
        <h3 className="m-3 scroll-m-20 text-xl text-blue-500 font-normal tracking-tight">
          Loading...
        </h3>
      </div>
    );
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between pl-6 pr-6 pb-8 gap-10">
      <Head>
        <title>News Aggregator</title>
      </Head>
      <div className="sticky top-0 bg-white z-40 w-full max-w-5xl items-center justify-between font-sans text-sm flex pt-4 md:pt-8 pb-4">
        <div className="flex flex-row gap-2 items-center text-lg font-semibold">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="w-6 h-6"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 7.5h1.5m-1.5 3h1.5m-7.5 3h7.5m-7.5 3h7.5m3-9h3.375c.621 0 1.125.504 1.125 1.125V18a2.25 2.25 0 01-2.25 2.25M16.5 7.5V18a2.25 2.25 0 002.25 2.25M16.5 7.5V4.875c0-.621-.504-1.125-1.125-1.125H4.125C3.504 3.75 3 4.254 3 4.875V18a2.25 2.25 0 002.25 2.25h13.5M6 7.5h3v3H6v-3z"
            />
          </svg>
          <p>News Aggregator</p>
        </div>
        <div>
          <a
            className="flex place-items-center lg:pointer-events-auto relative rounded bg-slate-100 py-[0.2rem] px-[0.3rem] font-mono text-sm font-semibold text-slate-900"
            href="https://lmuhacks.github.io/"
            target="_blank"
            rel="noopener noreferrer"
          >
            @lmu-hacks-2023
          </a>
        </div>
      </div>

      <div className="relative flex flex-col gap-16 items-center w-full max-w-4xl">
        <div className="flex flex-col items-center">
          <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">
            Today is {format(new Date(), 'MMMM do')}
          </h1>
          <h2 className="mt-4 scroll-m-20 text-slate-700 border-b-slate-700 pb-2 text-2xl lg:text-3xl font-semibold tracking-tight transition-colors first:mt-0">
            Paste in a news article below to begin
          </h2>
          {loading ? (
            <Loading />
          ) : (
            <div className="mt-3 w-full flex gap-2 items-center">
              <Input
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setUrl(e.target.value)}
                className="w-full"
                placeholder="Enter a news article link..."
              />
              <Button onClick={() => getSummary()} className="px-5 text-lg grid place-items-center">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="w-4 h-4"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3"
                  />
                </svg>
              </Button>
            </div>
          )}
        </div>
        <div className="w-full">
          <h3 className="mb-4 scroll-m-20 text-xl font-semibold tracking-tight">
            Or view suggested articles
          </h3>
          <Tabs defaultValue={categories[0]} className="w-full">
            <TabsList>
              {categories.map((category: string) => (
                <TabsTrigger key={category} value={category}>
                  {category}
                </TabsTrigger>
              ))}
            </TabsList>

            {categories.map((category: string) => (
              <TabsContent key={category + 'content'} value={category}>
                <p className="scroll-m-20 text-xl font-semibold tracking-tight">
                  Showing {category} articles
                </p>
                <div className="flex flex-row gap-4 flex-wrap mt-5">
                  <ArticleCard
                    key=" "
                    title="Lorem ipsum dolor..."
                    category={category}
                    date="Apr 12, 2023"
                  />
                  <ArticleCard
                    key=" "
                    title="Lorem ipsum dolor..."
                    category={category}
                    date="Apr 12, 2023"
                  />
                  <ArticleCard
                    key=" "
                    title="Lorem ipsum dolor..."
                    category={category}
                    date="Apr 12, 2023"
                  />
                  <ArticleCard
                    key=" "
                    title="Lorem ipsum dolor..."
                    category={category}
                    date="Apr 12, 2023"
                  />
                  <ArticleCard
                    key=" "
                    title="Lorem ipsum dolor..."
                    category={category}
                    date="Apr 12, 2023"
                  />
                  <ArticleCard
                    key=" "
                    title="Lorem ipsum dolor..."
                    category={category}
                    date="Apr 12, 2023"
                  />
                </div>
              </TabsContent>
            ))}
          </Tabs>
        </div>
      </div>

      <div className="grid text-center mb-0">
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Built by Lucian Prinz, Ari Kanevsky, Nicolas Ortiz, and Scott Nelson
        </p>
        <p className="text-sm text-slate-500 dark:text-slate-400 mt-2">
          Credit to
          <Link
            className="bg-transparent underline-offset-4 hover:underline text-slate-900 hover:bg-transparent px-1"
            href="https://ui.shadcn.com"
            target="_blank"
          >
            @shadcn
          </Link>
          for the UI components
        </p>
      </div>
    </main>
  );
}

